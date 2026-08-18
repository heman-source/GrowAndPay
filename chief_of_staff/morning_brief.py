#!/usr/bin/env python3
"""Chief of Staff — Daily Slack Morning Brief for Himanshu Sharma."""

import os
from datetime import datetime, timedelta, timezone

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import anthropic

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_USER_ID = os.environ["SLACK_USER_ID"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]

TARGET_CHANNELS = ["product", "leadership", "engineering", "general"]
LOOKBACK_HOURS = 24
IST = timezone(timedelta(hours=5, minutes=30))

slack = WebClient(token=SLACK_BOT_TOKEN)
claude = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def get_channel_id(name: str) -> str | None:
    try:
        for page in slack.conversations_list(types="public_channel,private_channel", limit=200):
            for ch in page["channels"]:
                if ch["name"].lower() == name.lower():
                    return ch["id"]
    except SlackApiError as e:
        print(f"Error listing channels: {e}")
    return None


def fetch_channel_messages(channel_id: str, oldest_ts: float) -> list[dict]:
    messages = []
    try:
        result = slack.conversations_history(channel=channel_id, oldest=str(oldest_ts), limit=200)
        messages = result.get("messages", [])
        for msg in list(messages):
            if msg.get("reply_count", 0) > 0:
                try:
                    thread = slack.conversations_replies(
                        channel=channel_id, ts=msg["ts"], oldest=str(oldest_ts), limit=50
                    )
                    messages.extend(thread.get("messages", [])[1:])
                except SlackApiError:
                    pass
    except SlackApiError as e:
        print(f"Error fetching from {channel_id}: {e}")
    return messages


def resolve_name(user_id: str, cache: dict) -> str:
    if user_id in cache:
        return cache[user_id]
    try:
        info = slack.users_info(user=user_id)
        name = info["user"].get("real_name") or info["user"].get("name", user_id)
    except SlackApiError:
        name = user_id
    cache[user_id] = name
    return name


def fetch_self_notes(oldest_ts: float) -> list[dict]:
    try:
        dm = slack.conversations_open(users=SLACK_USER_ID)
        dm_id = dm["channel"]["id"]
        result = slack.conversations_history(channel=dm_id, oldest=str(oldest_ts), limit=100)
        return [m for m in result.get("messages", []) if m.get("user") == SLACK_USER_ID]
    except SlackApiError as e:
        print(f"Could not fetch self-notes: {e}")
        return []


def format_channel(name: str, messages: list[dict], cache: dict) -> str:
    if not messages:
        return f"=== #{name.upper()} ===\n  (no messages)\n\n"
    lines = [f"=== #{name.upper()} ==="]
    for msg in sorted(messages, key=lambda m: float(m.get("ts", 0))):
        if msg.get("subtype"):
            continue
        text = msg.get("text", "").strip()
        if not text:
            continue
        user = resolve_name(msg.get("user", "unknown"), cache)
        ts = datetime.fromtimestamp(float(msg["ts"]), tz=timezone.utc).strftime("%H:%M UTC")
        is_reply = msg.get("thread_ts") and msg.get("thread_ts") != msg.get("ts")
        prefix = "  [thread] " if is_reply else "  "
        lines.append(f"{prefix}[{ts}] {user}: {text}")
    return "\n".join(lines) + "\n\n"


def generate_brief(channels_text: str, self_notes_text: str) -> str:
    today = datetime.now(IST).strftime("%A, %d %B %Y")
    response = claude.messages.create(
        model="claude-opus-4-5",
        max_tokens=2000,
        messages=[{
            "role": "user",
            "content": f"""You are the Chief of Staff for Himanshu Sharma, a product/engineering leader at AngelOne. Give him a crisp, zero-noise morning brief of Slack activity from the last 24 hours.

Today: {today}, 9:00 AM IST.

CHANNEL ACTIVITY:
{channels_text}

HIMANSHU'S SELF-NOTES (DMs to himself):
{self_notes_text or "No self-notes found."}

Write a structured brief with these sections (omit any section with nothing to report):

1. *🚨 Needs Your Attention* — Things requiring his decision, response, or action. Include any @mentions of him.

2. *✅ Decisions Made* — Key decisions taken (quote key phrases; attribute to person + channel).

3. *🔴 Escalations & Blockers* — Problems raised, things stuck, or issues flagged.

4. *📢 Important Announcements* — Strategic direction, policy changes, org updates.

5. *📝 From Your Notes* — Summary of what he noted for himself; flag overlaps with channel discussions.

6. *👀 Worth Knowing* — Signals or context worth tracking, even if no action needed.

Rules:
- Be specific; quote exact phrases for decisions/actions
- Attribute every item: who said it, which channel
- Skip small talk, status-only messages, and emoji reactions
- If a channel had nothing significant, write "[#channel] was quiet"
- End with one line: "Overall: Today looks [calm / busy / decision-heavy / …]"

Format for Slack mrkdwn: use *bold*, _italic_, and • bullets."""
        }]
    )
    return response.content[0].text


def send_dm(text: str):
    dm = slack.conversations_open(users=SLACK_USER_ID)
    channel_id = dm["channel"]["id"]
    ist_stamp = datetime.now(IST).strftime("%A, %d %B %Y · 9:00 AM IST")
    header = f"*🗞️ Chief of Staff Morning Brief*\n_{ist_stamp}_\n\n"
    full = header + text
    # Slack message limit is ~4000 chars; split if needed
    chunks = [full[i:i+3800] for i in range(0, len(full), 3800)]
    for chunk in chunks:
        slack.chat_postMessage(channel=channel_id, text=chunk, mrkdwn=True)
    print(f"Brief sent ({len(chunks)} message(s)).")


def main():
    now = datetime.now(timezone.utc)
    oldest_ts = (now - timedelta(hours=LOOKBACK_HOURS)).timestamp()
    cache: dict[str, str] = {}

    print("Fetching channel messages...")
    channels_text = ""
    for name in TARGET_CHANNELS:
        ch_id = get_channel_id(name)
        if not ch_id:
            print(f"  #{name}: not found or bot not a member")
            channels_text += f"=== #{name.upper()} ===\n  (channel not found or bot not added)\n\n"
            continue
        msgs = fetch_channel_messages(ch_id, oldest_ts)
        print(f"  #{name}: {len(msgs)} messages")
        channels_text += format_channel(name, msgs, cache)

    print("Fetching self-notes...")
    notes = fetch_self_notes(oldest_ts)
    self_notes_text = ""
    for m in sorted(notes, key=lambda x: float(x.get("ts", 0))):
        ts = datetime.fromtimestamp(float(m["ts"]), tz=timezone.utc).strftime("%H:%M UTC")
        self_notes_text += f"  [{ts}] {m.get('text', '').strip()}\n"

    print("Generating brief with Claude...")
    brief = generate_brief(channels_text, self_notes_text)

    print("Sending DM to Himanshu...")
    send_dm(brief)


if __name__ == "__main__":
    main()
