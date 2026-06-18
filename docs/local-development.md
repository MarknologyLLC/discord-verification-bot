# Local Development

## Setup

```bash
git clone https://github.com/MarknologyLLC/discord-verification-bot
cd discord-verification-bot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# fill in .env with your test server values
python bot.py
```

## Test server setup

Create a test Discord server with:
- A `#verification` channel (set as VERIFICATION_CHANNEL_ID)
- A `#staff-log` channel (set as STAFF_LOG_CHANNEL_ID)
- A `Verified Creator` role (set as VERIFIED_ROLE_ID)
- An `Admin` role (set as ADMIN_ROLE_ID)

## TikTok handle validation

Valid: `@username`, `https://www.tiktok.com/@username`
Invalid: `username` (no @ prefix, no URL)
