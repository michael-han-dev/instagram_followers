# Instagram Followers Manager

Tools to analyze and manage Instagram followers and following lists.

## Setup

1. Install dependencies:
```bash
pip install playwright python-dotenv
playwright install chromium
```

2. Create a `.env` file in the project root:
```
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
```

## Getting Your Follower/Following Lists

### Method 1: HTML Export (Recommended)

1. Request your Instagram data export:
   - Go to Instagram Settings → Privacy and Security → Download Your Data
   - Request "Followers and Following" data
   - Wait for email with download link

2. Extract the HTML files:
   - Download and unzip the export
   - Place HTML files in `connections/followers_and_following/`:
     - `followers_1.html`
     - `following.html`

3. Run the extractor:
```bash
python extract_usernames.py
```

This creates `followers_list.json` and `following_list.json`.

### Method 2: Live Scraping

1. Run the scraper:
```bash
python scrape_followers.py
```

2. The browser will open and log you in automatically.

3. **Two-Factor Authentication (2FA):**
   - If prompted, complete 2FA in the browser
   - Navigate to your profile page
   - **Open the followers modal** (click on your follower count)
   - Return to the terminal and press ENTER

4. The script will automatically scroll and collect all followers, saving to `followers_list.json`. If this doesn't work, manually scroll and the usernames will be logged.

**Note:** You'll need to manually export your following list from Instagram or use Method 1 for both lists.

## Comparing Lists

Analyze who follows you back and who doesn't:

```bash
python compare_followers.py
```

This shows:
- Total followers and following counts
- Mutual follows (both ways)
- Followers you don't follow back
- Accounts you follow who don't follow you back

## Unfollowing Accounts

### Interactive Selection (`unfollow_accounts.py`)

1. Run the script:
```bash
python unfollow_accounts.py
```

2. For each account that doesn't follow you back, you'll be prompted:
   - `y` - Add to unfollow list
   - `n` - Skip this account
   - `q` - Quit and proceed with selected accounts

3. After selecting accounts, confirm with `yes` to proceed.

4. **Two-Factor Authentication:**
   - Browser opens and logs in automatically
   - Complete 2FA if prompted
   - Dismiss any popups
   - Return to terminal and press ENTER

5. The script will unfollow selected accounts automatically.

### Batch Unfollow (`do_unfollow.py`)

For unfollowing from a pre-made list:

1. Create `accounts_to_unfollow.json` with a list of usernames:
```json
["username1", "username2", "username3"]
```

2. Run the script:
```bash
python do_unfollow.py
```

3. Confirm with `yes` when prompted.

4. **Two-Factor Authentication:**
   - Complete 2FA in the browser
   - Dismiss all popups
   - Press ENTER in terminal

5. The script unfollows all accounts in the list.

## Output Files

- `followers_list.json` - List of your followers
- `following_list.json` - List of accounts you follow
- `unfollowed_accounts.json` - Accounts successfully unfollowed
- `failed_to_unfollow.json` - Accounts that failed to unfollow

## Notes

- Scripts use slow, deliberate actions to avoid Instagram rate limits
- Keep the browser window visible during automation
- If a script fails, check the error messages and retry
- Instagram may show rate limit warnings; scripts include delays to minimize this

