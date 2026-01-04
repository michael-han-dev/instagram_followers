#!/usr/bin/env python3
# extract usernames from instagram html exports
# saves followers and following lists to json files

import re
import json
from pathlib import Path

def extract_usernames(html_file):
    content = Path(html_file).read_text(encoding='utf-8')
    pattern = r'href="https://www\.instagram\.com/([^"]+)"'
    usernames = re.findall(pattern, content)
    cleaned = []
    for u in usernames:
        if u.startswith('_u/'):
            cleaned.append(u[3:])
        else:
            cleaned.append(u)
    return sorted(set(cleaned))

def main():
    base_path = Path(__file__).parent
    html_path = base_path / "connections" / "followers_and_following"
    
    followers = extract_usernames(html_path / "followers_1.html")
    followers_file = base_path / "followers_list.json"
    with open(followers_file, 'w') as f:
        json.dump(followers, f, indent=2)
    print(f"Extracted {len(followers)} followers to {followers_file}")
    
    following = extract_usernames(html_path / "following.html")
    following_file = base_path / "following_list.json"
    with open(following_file, 'w') as f:
        json.dump(following, f, indent=2)
    print(f"Extracted {len(following)} following to {following_file}")

if __name__ == "__main__":
    main()

