# Chief of Staff — Morning Slack Brief

A daily workflow that sends Himanshu a structured AI-generated brief of important Slack activity from the last 24 hours. Runs every morning at 9:00 AM IST via GitHub Actions.

## What it does

1. Fetches messages from `#product`, `#leadership`, `#engineering`, and `#general`
2. Also reads any notes Himanshu sent to himself in Slack DMs
3. Uses Claude to identify: decisions made, action items, escalations, announcements, and signals worth knowing
4. Sends a formatted DM to Himanshu at 9:00 AM IST

## Setup

### 1. Create a Slack App

1. Go to [api.slack.com/apps](https://api.slack.com/apps) → **Create New App** → From scratch
2. Name it **"Chief of Staff"**, select your workspace
3. Under **OAuth & Permissions**, add these Bot Token Scopes:
   - `channels:history` — read public channel messages
   - `channels:read` — list channels
   - `groups:history` — read private channel messages
   - `groups:read` — list private channels
   - `im:history` — read DMs (for self-notes)
   - `im:write` — open DM conversations
   - `chat:write` — send DMs
   - `users:read` — resolve user names
4. Install the app to your workspace → copy the **Bot User OAuth Token** (`xoxb-…`)
5. Add the bot to each target channel: `/invite @Chief of Staff` in `#product`, `#leadership`, `#engineering`, `#general`

### 2. Get your Slack User ID

In Slack: click your profile → **View profile** → **More** → copy the Member ID (format: `U01XXXXXXX`)

### 3. Add GitHub Secrets

In the repo: **Settings → Secrets and variables → Actions → New repository secret**

| Secret name | Value |
|---|---|
| `SLACK_BOT_TOKEN` | The `xoxb-…` bot token from step 1 |
| `SLACK_USER_ID` | Your Slack Member ID from step 2 |
| `ANTHROPIC_API_KEY` | Your Anthropic API key |

### 4. Test it

Go to **Actions → Chief of Staff Morning Brief → Run workflow** to trigger manually.

## Schedule

The workflow runs on cron `30 3 * * *` (UTC), which is **9:00 AM IST** every day.
