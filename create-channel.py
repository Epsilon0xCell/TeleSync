import os
from datetime import datetime

from telethon import TelegramClient, functions

# Get API credentials from https://my.telegram.org and provide them as
# environment variables (or replace the defaults with your values here).
api_id = int(os.environ.get("TELEGRAM_API_ID", "0"))
api_hash = os.environ.get("TELEGRAM_API_HASH", "")
phone = os.environ.get("TELEGRAM_PHONE", "")

if not api_id or not api_hash:
    raise SystemExit(
        "Set TELEGRAM_API_ID and TELEGRAM_API_HASH first "
        "(see https://my.telegram.org)."
    )

client = TelegramClient('session_name', api_id, api_hash)

async def main():
    # Login to Telegram
    await client.start(phone)

    # Create the channel name
    channel_name = f"backup-{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # Create the channel
    result = await client(functions.channels.CreateChannelRequest(
        title=channel_name,
        about="Backup channel",
        megagroup=False
    ))

    # Get the invite link to the channel
    invite_link = await client(functions.messages.ExportChatInviteRequest(result.chats[0].id))

    # Store the invite link in a text file
    with open("channel_invite_link.txt", "w") as f:
        f.write(f"{invite_link.link}\n")

    # Print the result
    print(f"Channel '{result.chats[0].title}' (id: {result.chats[0].id}) created successfully.")
    print(f"Invite link: {invite_link.link}")

    # Logout
    await client.disconnect()

with client:
    client.loop.run_until_complete(main())
