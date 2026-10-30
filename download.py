# I keep the download side in its own tiny script because I run it by
# hand, on a different day from the backup run, when I actually need a
# file back.
import os
import subprocess

# Check if telegram_downloads directory exists, if not create it
if not os.path.exists('telegram_downloads'):
    os.mkdir('telegram_downloads')

# Switch to telegram_downloads directory
# I change into the folder before running the tool because
# telegram-download writes into its working directory. There is no
# output path setting I rely on, so the working directory is the
# setting.
os.chdir('telegram_downloads')

# Run the telegram-download --interactive command
# I keep this interactive on purpose. I pick files by hand from the
# channel, and a blind full download would pull every old backup down
# again each time I only need one of them back.
subprocess.run(['telegram-download', '--interactive'])
