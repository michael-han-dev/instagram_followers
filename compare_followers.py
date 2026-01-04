#!/usr/bin/env python3
# compare instagram followers and following lists
# find accounts that don't follow back

import json
from pathlib import Path

def main():
    base_path = Path(__file__).parent
    
    followers_file = base_path / "followers_list.json"
    if not followers_file.exists():
        print(f"Error: {followers_file} not found. Run extract_usernames.py first.")
        return
    with open(followers_file, 'r') as f:
        followers = set(json.load(f))
    
    following_file = base_path / "following_list.json"
    if not following_file.exists():
        print(f"Error: {following_file} not found. Run extract_usernames.py first.")
        return
    with open(following_file, 'r') as f:
        following = set(json.load(f))
    
    print(f"Total Followers: {len(followers)}")
    print(f"Total Following: {len(following)}")
    print()
    
    mutual = followers & following
    print(f"Mutual (follow each other): {len(mutual)}")
    print()
    
    followers_only = followers - following
    print(f"=== FOLLOWERS YOU DON'T FOLLOW BACK ({len(followers_only)}) ===")
    for username in sorted(followers_only):
        print(f"  @{username}")
    print()
    
    following_only = following - followers
    print(f"=== FOLLOWING WHO DON'T FOLLOW YOU BACK ({len(following_only)}) ===")
    for username in sorted(following_only):
        print(f"  @{username}")

if __name__ == "__main__":
    main()
