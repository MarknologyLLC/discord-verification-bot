# Discord Server Setup

Before production launch, confirm all of the following.

## Bot intents (Discord Developer Portal)

- [ ] **Server Members Intent** -- enabled (bot needs member data)
- [ ] **Message Content Intent** -- enabled (bot reads typed answers in ticket channels)

## Bot role position

- [ ] Bot role is **above** the Verified Creator role in the server role list
  (required for the bot to assign that role via /approve)

## Bot permissions

Minimum required:
- Manage Channels (create/delete ticket channels)
- Send Messages
- Embed Links
- Read Message History
- Manage Roles (assign verified role)
- View Channels

Do not grant Administrator. Scope permissions to the minimum needed.

## Slash command setup

Run these in the verification channel after bot starts:

- [ ] `/setup_verification` posts the application panel
- [ ] `/approve @member` works for staff role
- [ ] `/close` works for staff role in a ticket channel
- [ ] `/export_creators` works for admin role only

## Channel/category structure

- A public verification channel (set as the panel target)
- A private staff log channel (set as LOG_CHANNEL_ID)
- A category for pending ticket channels (set as PENDING_CATEGORY_ID)
