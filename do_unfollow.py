#!/usr/bin/env python3
# automated unfollow script for instagram accounts
# reads accounts from accounts_to_unfollow.json and unfollows them

import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

INSTAGRAM_USERNAME = "YOUR_USERNAME"
INSTAGRAM_PASSWORD = "YOUR_PASSWORD"

def main():
    base_path = Path(__file__).parent
    accounts_file = base_path / "accounts_to_unfollow.json"
    
    with open(accounts_file, "r") as f:
        accounts = json.load(f)
    
    print(f"Loaded {len(accounts)} accounts to unfollow")
    
    confirm = input(f"\nUnfollow all {len(accounts)} accounts? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Cancelled.")
        return
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page = context.new_page()
        
        page.goto("https://www.instagram.com/accounts/login/")
        page.wait_for_load_state("networkidle")
        time.sleep(2)
        
        page.fill('input[name="username"]', INSTAGRAM_USERNAME)
        page.fill('input[name="password"]', INSTAGRAM_PASSWORD)
        page.click('button[type="submit"]')
        page.wait_for_load_state("networkidle")
        
        input(">>> Complete 2FA, dismiss ALL popups, then press ENTER...")
        
        unfollowed = []
        failed = []
        
        for i, username in enumerate(accounts, 1):
            print(f"[{i}/{len(accounts)}] @{username}...", end=" ", flush=True)
            
            try:
                page.goto(f"https://www.instagram.com/{username}/", timeout=20000)
                time.sleep(3)
                
                clicked = page.evaluate("""
                    () => {
                        const buttons = document.querySelectorAll('button');
                        for (const btn of buttons) {
                            const text = btn.textContent.trim();
                            if (text === 'Following' || text.includes('Following')) {
                                btn.click();
                                return true;
                            }
                        }
                        const divs = document.querySelectorAll('div[role="button"]');
                        for (const div of divs) {
                            if (div.textContent.includes('Following')) {
                                div.click();
                                return true;
                            }
                        }
                        return false;
                    }
                """)
                
                if clicked:
                    time.sleep(2)
                    
                    unfollow_clicked = page.evaluate("""
                        () => {
                            const all = document.querySelectorAll('button, div, span');
                            for (const el of all) {
                                if (el.textContent.trim() === 'Unfollow' && el.offsetParent !== null) {
                                    el.click();
                                    return true;
                                }
                            }
                            const buttons = document.querySelectorAll('button');
                            for (const btn of buttons) {
                                if (btn.textContent.includes('Unfollow')) {
                                    btn.click();
                                    return true;
                                }
                            }
                            return false;
                        }
                    """)
                    
                    if unfollow_clicked:
                        time.sleep(1)
                        unfollowed.append(username)
                        print("✓")
                    else:
                        failed.append(username)
                        print("✗ no unfollow btn")
                else:
                    print("- skip")
                    
            except Exception as e:
                failed.append(username)
                print(f"✗ {str(e)[:30]}")
        
        browser.close()
    
    print(f"\nDone! Unfollowed: {len(unfollowed)} | Failed: {len(failed)}")
    
    if unfollowed:
        with open(base_path / "unfollowed_accounts.json", "w") as f:
            json.dump(unfollowed, f, indent=2)
    
    if failed:
        with open(base_path / "failed_to_unfollow.json", "w") as f:
            json.dump(failed, f, indent=2)

if __name__ == "__main__":
    main()
