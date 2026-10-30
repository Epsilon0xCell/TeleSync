# I keep this step in its own script on purpose. Making a channel is a
# one time setup act, while uploading is the repeat act. upload.py only
# needs the invite link file that this script leaves behind.
import os
from datetime import datetime

from telethon import TelegramClient, functions

# Get API credentials from https://my.telegram.org and provide them as
# environment variables (or replace the defaults with your values here).
# I convert the id to int at load time. Telethon rejects a string id in
# a confusing way much later, and a missing variable becomes 0 here,
# which the guard below treats as not set.
api_id = int(os.environ.get("TELEGRAM_API_ID", "0"))
api_hash = os.environ.get("TELEGRAM_API_HASH", "")
phone = os.environ.get("TELEGRAM_PHONE", "")

if not api_id or not api_hash:
    raise SystemExit(
        "Set TELEGRAM_API_ID and TELEGRAM_API_HASH first "
        "(see https://my.telegram.org)."
    )

# I use a fixed session name. Telethon writes session_name.session next
# to this script, and reusing that file means I log in once instead of
# getting a code prompt on every run.
client = TelegramClient('session_name', api_id, api_hash)

async def main():
    # Login to Telegram
    await client.start(phone)

    # Create the channel name
    # I put the time down to the second in the name. I make one channel
    # per backup run, and two runs close together still need names that
    # do not collide when I look at the channel list later.
    channel_name = f"backup-{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # Create the channel
    # megagroup=False asks for a channel, not a group. This is a one way
    # drop box for my files, and nobody needs to post replies inside it.
    result = await client(functions.channels.CreateChannelRequest(
        title=channel_name,
        about="Backup channel",
        megagroup=False
    ))

    # Get the invite link to the channel
    invite_link = await client(functions.messages.ExportChatInviteRequest(result.chats[0].id))

    # Store the invite link in a text file
    # I hand the link over through a plain file because upload.py is a
    # separate process with no shared memory. The file is the whole
    # handoff, and the newline I add here is why upload.py strips the
    # line it reads back.
    with open("channel_invite_link.txt", "w") as f:
        f.write(f"{invite_link.link}\n")

    # Print the result
    print(f"Channel '{result.chats[0].title}' (id: {result.chats[0].id}) created successfully.")
    print(f"Invite link: {invite_link.link}")

    # Logout
    await client.disconnect()

# I run main inside the client context so the connection still closes
# when main raises partway. The disconnect at the end of main only
# covers the clean path.
with client:
    client.loop.run_until_complete(main())
