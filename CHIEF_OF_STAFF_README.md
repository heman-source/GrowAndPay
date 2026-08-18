# Slack Chief of Staff — Morning Brief

A daily automated brief delivered to your Slack DM at 9:00 AM IST (Mon–Fri).

## What it does

Scans the last 24 hours of #product, #leadership, #engineering, and #general,
plus your personal Slack notes (messages you sent to yourself), then uses Claude
to distill everything into a 3-minute morning read covering:

- Key decisions made
- Action items for you or your team
- Escalations & blockers
- Important announcements
- Your personal notes from the previous day
- Things to keep an eye on

## Setup (one-time)

### 1. Create a Slack App

1. Go to https://api.slack.com/apps → **Create New App** → From scratch
2. Name it "Chief of Staff", pick your workspace
3. Under **OAuth & Permissions**, add these Bot Token Scopes:
   - `channels:history` — read public channels
   - `channels:join` — join public channels to read them
   - `groups:history` — read private channels the bot is in
   - `im:history` — read DMs (for your personal notes)
   - `im:write` — open DM to deliver the brief
   - `users:read` — resolve usernames
   - `chat:write` — post the brief
4. **Install App** to workspace → copy the **Bot User OAuth Token** (`xoxb-...`)
5. Invite the bot to each channel: `/invite @Chief of Staff` in #product, #leadership, #engineering, #general

### 2. Find your Slack User ID

In Slack: click your profile → **More** → Copy Member ID (format: `U01ABC123`)

### 3. Add GitHub Secrets

In your repo → **Settings** → **Secrets and variables** → **Actions**:

| Secret | Value |
|--------|-------|
| `SLACK_BOT_TOKEN` | `xoxb-...` from step 1 |
| `ANTHROPIC_API_KEY` | Your Anthropic API key |
| `SLACK_USER_ID` | Your Slack user ID from step 2 |

### 4. Enable the workflow

The cron job runs automatically Mon–Fri at 3:30 AM UTC (9:00 AM IST).

To test immediately: **Actions** tab → **Morning Chief of Staff Brief** → **Run workflow**

## Sample output format

```
🌅 Good morning, Himanshu! Here's your Chief of Staff brief for Monday, 18 August 2025.

📌 KEY DECISIONS MADE
• [#product] Priya confirmed moving the Holdings redesign to Sprint 23 (start date: Aug 25)
• [#leadership] CTO approved headcount for 2 senior engineers in the Data Platform team

⚡ ACTION ITEMS FOR YOU / YOUR TEAM
• Review the Grow & Pay PRD draft shared by Rohan — feedback requested by EOD today
• Approve Q3 OKR rollup before Thursday's all-hands

🚨 ESCALATIONS & BLOCKERS
• [#engineering] API rate limits on NSE feed causing intermittent failures since 11 PM yesterday — Aditya is on it but may need infra decision

📢 IMPORTANT ANNOUNCEMENTS
• Company-wide offsite confirmed for Sep 12–13 in Lonavala — logistics in #general

💬 YOUR PERSONAL NOTES
• "Follow up with Ravi on broker tie-up for Q4"
• "Check on NPS dashboard metrics before the board deck"

🔍 THINGS TO KEEP AN EYE ON
• Discussion in #product about deprecating the old watchlist API — no decision yet but 3 PMs are aligned
```
