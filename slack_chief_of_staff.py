import os
import time
from datetime import datetime, timedelta, timezone
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import anthropic

SLACK_TOKEN = os.environ["SLACK_BOT_TOKEN"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
TARGET_USER_ID = os.environ["SLACK_USER_ID"]

CHANNELS_TO_SCAN = ["product", "leadership", "engineering", "general"]
LOOKBACK_HOURS = 24

slack = WebClient(token=SLACK_TOKEN)
claude = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def get_channel_id(name: str) -> str | None:
    cursor = None
    while True:
        resp = slack.conversations_list(
            types="public_channel,private_channel",
            limit=200,
            cursor=cursor,
        )
        for ch in resp["channels"]:
            if ch["name"] == name:
                return ch["id"]
        cursor = resp.get("response_metadata", {}).get("next_cursor")
        if not cursor:
            return None


def fetch_messages(channel_id: str, oldest: float) -> list[dict]:
    messages = []
    cursor = None
    while True:
        try:
            resp = slack.conversations_history(
                channel=channel_id,
                oldest=str(oldest),
                limit=200,
                cursor=cursor,
            )
            messages.extend(resp.get("messages", []))
            cursor = resp.get("response_metadata", {}).get("next_cursor")
            if not cursor:
                break
        except SlackApiError as e:
            if e.response["error"] == "not_in_channel":
                slack.conversations_join(channel=channel_id)
                continue
            break
    return messages


def resolve_username(user_id: str, cache: dict) -> str:
    if user_id in cache:
        return cache[user_id]
    try:
        info = slack.users_info(user=user_id)
        name = info["user"].get("real_name") or info["user"].get("name", user_id)
        cache[user_id] = name
        return name
    except SlackApiError:
        cache[user_id] = user_id
        return user_id


def fetch_self_notes(user_id: str, oldest: float) -> list[str]:
    """Fetch messages the user sent to themselves (personal notes)."""
    try:
        resp = slack.conversations_open(users=user_id)
        dm_id = resp["channel"]["id"]
        msgs = fetch_messages(dm_id, oldest)
        return [m["text"] for m in msgs if m.get("user") == user_id and m.get("text")]
    except SlackApiError:
        return []


def collect_all_messages() -> dict[str, list[str]]:
    cutoff = time.time() - LOOKBACK_HOURS * 3600
    user_cache: dict[str, str] = {}
    channel_messages: dict[str, list[str]] = {}

    for channel_name in CHANNELS_TO_SCAN:
        ch_id = get_channel_id(channel_name)
        if not ch_id:
            channel_messages[channel_name] = []
            continue

        raw_msgs = fetch_messages(ch_id, cutoff)
        formatted = []
        for m in raw_msgs:
            if not m.get("text") or m.get("subtype"):
                continue
            user = resolve_username(m.get("user", "unknown"), user_cache)
            ts = datetime.fromtimestamp(float(m["ts"]), tz=timezone.utc).strftime("%H:%M UTC")
            formatted.append(f"[{ts}] {user}: {m['text']}")

        channel_messages[channel_name] = formatted

    self_notes = fetch_self_notes(TARGET_USER_ID, cutoff)
    if self_notes:
        channel_messages["your-notes"] = self_notes

    return channel_messages


def build_brief(channel_messages: dict[str, list[str]]) -> str:
    sections = []
    for channel, messages in channel_messages.items():
        if messages:
            block = f"=== #{channel} ({len(messages)} messages) ===\n" + "\n".join(messages)
            sections.append(block)

    if not sections:
        return "No messages found in the last 24 hours."

    raw_dump = "\n\n".join(sections)
    today = datetime.now(timezone.utc).strftime("%A, %d %B %Y")

    prompt = f"""You are the Chief of Staff for Himanshu Sharma at Angel One (a stock brokerage).
Today is {today}. Below are the last 24 hours of Slack messages from key channels.

Your job: produce a crisp morning brief that Himanshu can read in under 3 minutes.

Structure your response EXACTLY like this:

🌅 *Good morning, Himanshu! Here's your Chief of Staff brief for {today}.*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 *KEY DECISIONS MADE*
List each decision with: channel, who decided, what was decided. If none, write "None".

⚡ *ACTION ITEMS FOR YOU / YOUR TEAM*
List each action item. Flag if it has a deadline. If none, write "None".

🚨 *ESCALATIONS & BLOCKERS*
Anything urgent that needs your attention today. If none, write "None".

📢 *IMPORTANT ANNOUNCEMENTS*
Leadership updates, org changes, launches, major milestones. If none, write "None".

💬 *YOUR PERSONAL NOTES (from yesterday)*
Summarize any notes Himanshu left for himself. If none, write "None".

🔍 *THINGS TO KEEP AN EYE ON*
Ongoing discussions or emerging issues that don't need action today but are worth monitoring.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
_Brief covers: last 24 hours | Channels: #product #leadership #engineering #general_

Be direct and specific. Use names. Don't hedge. If something is unclear, skip it rather than guess.

RAW MESSAGES:
{raw_dump}
"""

    response = claude.messages.create(
        model="claude-opus-5-20251101",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def send_dm(user_id: str, text: str):
    resp = slack.conversations_open(users=user_id)
    channel_id = resp["channel"]["id"]
    slack.chat_postMessage(channel=channel_id, text=text, mrkdwn=True)


def main():
    print("Collecting messages from the last 24 hours...")
    channel_messages = collect_all_messages()

    total = sum(len(v) for v in channel_messages.values())
    print(f"Fetched {total} messages across {len(channel_messages)} channels/DMs.")

    print("Generating brief with Claude...")
    brief = build_brief(channel_messages)

    print("Sending DM to user...")
    send_dm(TARGET_USER_ID, brief)
    print("Done. Morning brief delivered.")


if __name__ == "__main__":
    main()
