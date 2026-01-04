#!/usr/bin/env python3
# interactive unfollow script for accounts that don't follow back
# prompts user to select accounts and then unfollows them

import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

INSTAGRAM_USERNAME = "YOUR_USERNAME"
INSTAGRAM_PASSWORD = "YOUR_PASSWORD"

def get_non_followers():
    base_path = Path(__file__).parent
    
    with open(base_path / "followers_list.json", "r") as f:
        followers = set(json.load(f))
    
    with open(base_path / "following_list.json", "r") as f:
        following = set(json.load(f))
    
    return sorted(following - followers)

def select_accounts_to_unfollow(non_followers):
    to_unfollow = []
    total = len(non_followers)
    
    print(f"\nFOLLOWING WHO DON'T FOLLOW YOU BACK ({total})")
    print("=" * 50)
    print("Enter 'y' to unfollow, 'n' to skip, 'q' to quit and proceed\n")
    
    for i, username in enumerate(non_followers, 1):
        response = input(f"[{i}/{total}] @{username} - unfollow? (y/n/q): ").strip().lower()
        
        if response == "q":
            break
        if response == "y":
            to_unfollow.append(username)
            print(f"  -> Added to unfollow list ({len(to_unfollow)} selected)")
    
    return to_unfollow

def unfollow_accounts(accounts):
    if not accounts:
        print("No accounts to unfollow.")
        return
    
    print(f"\nWill unfollow {len(accounts)} accounts:")
    for acc in accounts:
        print(f"  @{acc}")
    
    confirm = input("\nProceed? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Cancelled.")
        return
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        page = context.new_page()
        
        page.goto("https://www.instagram.com/accounts/login/")
        page.wait_for_load_state("networkidle")
        time.sleep(2)
        
        page.fill('input[name="username"]', INSTAGRAM_USERNAME)
        page.fill('input[name="password"]', INSTAGRAM_PASSWORD)
        page.click('button[type="submit"]')
        page.wait_for_load_state("networkidle")
        
        input(">>> Complete 2FA if needed, then press ENTER to start unfollowing...")
        
        unfollowed = []
        failed = []
        
        for i, username in enumerate(accounts, 1):
            print(f"[{i}/{len(accounts)}] Unfollowing @{username}...")
            
            try:
                page.goto(f"https://www.instagram.com/{username}/")
                page.wait_for_load_state("networkidle")
                time.sleep(2)
                
                following_btn = page.locator('button:has-text("Following")').first
                if following_btn.is_visible():
                    following_btn.click()
                    time.sleep(1)
                    
                    unfollow_btn = page.locator('button:has-text("Unfollow")').first
                    if unfollow_btn.is_visible():
                        unfollow_btn.click()
                        time.sleep(2)
                        unfollowed.append(username)
                        print(f"  -> Unfollowed")
                    else:
                        failed.append(username)
                        print(f"  -> Failed: Unfollow button not found")
                else:
                    failed.append(username)
                    print(f"  -> Skipped: Not following or button not found")
                
                time.sleep(1)
                
            except Exception as e:
                failed.append(username)
                print(f"  -> Error: {e}")
        
        browser.close()
    
    print(f"\nDone! Unfollowed {len(unfollowed)} accounts.")
    if failed:
        print(f"Failed: {len(failed)} - {failed}")
    
    output_file = Path(__file__).parent / "unfollowed_accounts.json"
    with open(output_file, "w") as f:
        json.dump(unfollowed, f, indent=2)
    print(f"Saved unfollowed list to {output_file}")

def main():
    non_followers = get_non_followers()
    print(f"Found {len(non_followers)} accounts you follow who don't follow back.")
    
    to_unfollow = select_accounts_to_unfollow(non_followers)
    
    if to_unfollow:
        print(f"\nSelected {len(to_unfollow)} accounts to unfollow.")
        unfollow_accounts(to_unfollow)
    else:
        print("\nNo accounts selected to unfollow.")

if __name__ == "__main__":
    main()

