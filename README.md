# Marknology Discord Verification Bot

Handles creator applications for the Marknology TikTok Shop creator community on Discord.

## What it does

- Posts a public verification panel with a "Create ticket" button
- Opens a private ticket channel for each applicant
- Walks applicants through questions one at a time:
  1. Email
  2. First and last name
  3. TikTok handle
  4. How they heard about us
- Validates TikTok handles (@username and profile URLs pass, bare usernames rejected)
- Saves completed applications
- Posts completed applications to a staff log channel
- `/approve @member` -- grants the verified role
- `/close` -- closes and deletes the ticket channel
- `/export_creators` -- admin-only export of applications

## Repo structure

```
discord-verification-bot/
  bot.py                  -- main bot entry point
  requirements.txt        -- Python dependencies
  .env.example            -- environment variable template (no secrets)
  .gitignore              -- keeps secrets and applicant data out of git
  docs/
    deployment.md         -- how to deploy
    local-development.md  -- how to run locally
    review-process.md     -- PR review gate with Winston
```

## Security rules

- Never commit `.env`
- Never commit real bot tokens, Discord tokens, server IDs, role IDs, or channel IDs
- Never commit `creators.json` (contains applicant emails -- private)
- Never commit exported applicant files

## Development workflow

Paul Baron (PaulbCatalyst) builds via Codex and opens PRs here.
Winston (MarknologyLLC) reviews every PR automatically.
Drew approves and squash merges after APPROVED verdict.
Review results post to `#dev-collab` in Marknology HQ Discord.

## Setup

```bash
cp .env.example .env
# fill in your values
pip install -r requirements.txt
python bot.py
```
