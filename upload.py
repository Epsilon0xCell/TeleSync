# python script to upload files inside the encrypted_zips directory one by one to telegram individually using a loop when running for the first time it will ask you to give your tokens
import subprocess
import sys

# I shell out to telegram-upload here instead of driving Telethon the
# way create-channel.py does. That tool already handles large files and
# prints file ids, and I do not want a second upload engine to maintain
# in this file.
try:
    with open("channel_invite_link.txt", "r") as f:
        # I read only the first line. create-channel.py writes one link
        # plus a newline, so anything past the first line in that file
        # is not part of the link I should send to.
        invite_link = f.readline().strip()
except FileNotFoundError:
    sys.exit("channel_invite_link.txt not found. Run create-channel.py first to create the backup channel.")

# I build this as one shell string because the ** pattern has to reach
# telegram-upload as an argument shape it understands on Windows.
# --large-files=split is my second guard, after main.ps1, for a volume
# that still comes out over the Telegram size limit, and the thumbnail
# is the preview image that already ships in this repo.
command = f"telegram-upload .\\encrypted_zips\\** --to {invite_link} --large-files=split --print-file-id --thumbnail-file=.\\preview.png"
# I do not check the exit code here. A failed upload prints its own
# error from telegram-upload, and this script keeps no retry state to
# act on. I accept that gap instead of pretending a rerun is a plan.
subprocess.run(command, shell=True)
