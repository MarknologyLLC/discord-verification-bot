# Deployment

## Requirements
- Python 3.11+
- A Discord bot token with these intents enabled: `message_content`, `members`
- Bot invited to your server with: Manage Channels, Send Messages, Embed Links, Attach Files, Read Message History, Manage Roles

## Steps

1. Clone the repo
2. `cp .env.example .env` and fill in all values
3. `pip install -r requirements.txt`
4. `python bot.py`

## Environment variables

See `.env.example` for all required values.

## Security

- `creators.json` is gitignored and contains applicant emails. Keep it private.
- Never share your `.env` file.
- Export files from `/export_creators` are ephemeral -- not saved to the repo.
