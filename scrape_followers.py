#!/usr/bin/env python3
# scrape instagram followers using playwright
# saves the list to followers_list.json

import json
import os
import time
from pathlib import Path
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()

INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

def scrape_followers():
    followers = set()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        page.goto("https://www.instagram.com/accounts/login/")
        page.wait_for_load_state("networkidle")
        time.sleep(2)
        
        page.fill('input[name="username"]', INSTAGRAM_USERNAME)
        page.fill('input[name="password"]', INSTAGRAM_PASSWORD)
        page.click('button[type="submit"]')
        page.wait_for_load_state("networkidle")
        time.sleep(3)
        
        input(">>> Complete login, navigate to your profile, and OPEN THE FOLLOWERS MODAL. Then press ENTER here...")
        
        last_count = 0
        no_change_count = 0
        
        while no_change_count < 10:
            usernames = page.evaluate("""
                () => {
                    const dialog = document.querySelector('div[role="dialog"]');
                    if (!dialog) return [];
                    const links = dialog.querySelectorAll('a[href^="/"]');
                    const names = [];
                    links.forEach(link => {
                        const href = link.getAttribute('href');
                        if (href && href.match(/^\/[^\/]+\/$/)) {
                            const username = href.replace(/\//g, '');
                            if (username) names.push(username);
                        }
                    });
                    return names;
                }
            """)
            
            for username in usernames:
                if username != INSTAGRAM_USERNAME:
                    followers.add(username)
            
            current_count = len(followers)
            print(f"Found {current_count} followers...")
            
            if current_count == last_count:
                no_change_count += 1
            else:
                no_change_count = 0
            last_count = current_count
            
            page.evaluate("""
                () => {
                    const dialog = document.querySelector('div[role="dialog"]');
                    if (!dialog) return;
                    const scrollable = dialog.querySelector('div[style*="overflow: hidden auto"]') 
                        || dialog.querySelector('div[style*="overflow-y: auto"]')
                        || dialog.querySelector('._aano');
                    if (scrollable) {
                        scrollable.scrollTop = scrollable.scrollHeight;
                    } else {
                        const inner = dialog.querySelector('div > div > div');
                        if (inner) inner.scrollTop = inner.scrollHeight;
                    }
                }
            """)
            time.sleep(1.5)
        
        browser.close()
    
    return sorted(followers)

def main():
    if not INSTAGRAM_USERNAME or not INSTAGRAM_PASSWORD:
        print("Error: Set INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD environment variables.")
        return
    
    print(f"Scraping followers for @{INSTAGRAM_USERNAME}...")
    followers = scrape_followers()
    
    output_file = Path(__file__).parent / "followers_list.json"
    with open(output_file, "w") as f:
        json.dump(followers, f, indent=2)
    
    print(f"Saved {len(followers)} followers to {output_file}")

if __name__ == "__main__":
    main()

