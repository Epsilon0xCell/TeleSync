@echo off
cd /d "%~dp0"

:: I put the admin gate once, before the loop, not inside it. Inside
:: the loop it would ask again on every cycle, and this file exists to
:: run alone for days at a time.
:: Check if the script is running as administrator
NET SESSION >NUL 2>&1
IF %ERRORLEVEL% EQU 0 (
    goto loop
) ELSE (
    echo You need to run this script as an administrator
    pause
    exit /b 1
)

:loop
:: I run the three steps in this order because each one eats the
:: output of the step before it. main.ps1 makes the archive,
:: create-channel.py makes the channel and the link file, and
:: upload.py sends the archive to that channel.
powershell ./main.ps1
python create-channel.py
python upload.py
:: 86400 seconds is 24 hours, and I count it from the end of an
:: upload, not from a fixed clock time. A slow upload pushes the next
:: run later instead of stacking two runs on top of each other.
timeout /t 86400 /nobreak >nul
goto loop
