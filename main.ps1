# Define the name of the folder to create
$folderName = "encrypted_zips"

# Get the current working directory
$currentDirectory = Get-Location

# Build the full path to the folder to create
$folderPath = Join-Path $currentDirectory $folderName

# Check if the folder already exists and delete it if it does
if (Test-Path $folderPath) {
    Remove-Item $folderPath -Recurse
}

# Create the folder
New-Item -ItemType Directory -Path $folderPath

# Define the name of the folder to compress and encrypt
$folderToCompressName = "sync"

# Build the path to the folder to compress and encrypt
$folderToCompressPath = Join-Path $currentDirectory $folderToCompressName

# Check if the folder to compress and encrypt exists and create it if it doesn't
if (-not (Test-Path $folderToCompressPath)) {
    New-Item -ItemType Directory -Path $folderToCompressPath
}

# Build the path to the output file
$outputFilePath = Join-Path $folderPath "sync.7z"

# Build the path to the 7-Zip executable
$sevenZipPath = "C:\Program Files\7-Zip\7z.exe"

# Stop early if 7-Zip is not installed where the script expects it
if (-not (Test-Path $sevenZipPath)) {
    Write-Host "7-Zip was not found at $sevenZipPath. Install 7-Zip first: https://7-zip.org/download.html"
    exit 1
}

# Ask for the passwords at run time. Passwords are never stored in this script.
# Back the passwords up somewhere safe and private: without them the archive cannot be opened.
$archivePasswordSecure = Read-Host "Enter the password for the archive" -AsSecureString
$archivePassword = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($archivePasswordSecure))
if ([string]::IsNullOrEmpty($archivePassword)) {
    Write-Host "A password is required."
    exit 1
}

# A large archive that gets split can use a second password for the split volumes.
# Leave the second prompt blank to reuse the archive password.
$splitPasswordSecure = Read-Host "Enter the password for the split volumes (leave blank to reuse the archive password)" -AsSecureString
$splitPassword = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($splitPasswordSecure))
if ([string]::IsNullOrEmpty($splitPassword)) {
    $splitPassword = $archivePassword
}

# Compress and encrypt the folder using 7-Zip
& $sevenZipPath a -t7z -m0=lzma2 -mx=9 -mfb=273 -md=256m -ms=on -p"$archivePassword" -mhe=on $outputFilePath $folderToCompressPath

# Stop early if 7-Zip did not produce the archive
if (-not (Test-Path $outputFilePath)) {
    Write-Host "7-Zip did not create $outputFilePath. Nothing was uploaded or split."
    exit 1
}

# Check if the output file is larger than 1.9GB and split it if necessary
$maxFileSize = 1.9GB

if ((Get-Item $outputFilePath).Length -gt $maxFileSize) {
    $outputFileBaseName = [System.IO.Path]::GetFileNameWithoutExtension($outputFilePath)
    $outputFileExtension = [System.IO.Path]::GetExtension($outputFilePath)

    # Split the file using 7-Zip, into volumes of at most 1900 MB each
    & $sevenZipPath a -t7z -m0=lzma2 -mx=9 -mfb=273 -md=256m -ms=on "-v1900m" -p"$splitPassword" -mhe=on "${outputFilePath}.split" "${outputFilePath}"

    # Delete the original file
    Remove-Item $outputFilePath

    # Notify the user about the output file location and size
    Write-Host "The compressed and encrypted file(s) are located in:" $folderPath
    $outputFiles = Get-ChildItem $folderPath -Filter "${outputFileBaseName}${outputFileExtension}.split.*"
    foreach ($outputFile in $outputFiles) {
            $fileSize = "{0:N2}" -f ($outputFile.Length / 1MB)
            Write-Host $outputFile.Name " " $fileSize " MB"
    }
}
elseif ((Get-Item $outputFilePath).Length -le $maxFileSize) {
    # Notify the user about the output file location and size
    Write-Host "The compressed and encrypted file is located in:" $outputFilePath
    $outputFile = Get-Item $outputFilePath
    Write-Host "$($outputFile.Name) $($("{0:N2}" -f ($outputFile.Length / 1MB))) MB"
}
