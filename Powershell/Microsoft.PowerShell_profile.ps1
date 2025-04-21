
# Import-Module posh-git # Redundant with Oh-My-Posh

# Icons in PS
Import-Module -Name Terminal-Icons #Install-Module -Name Terminal-Icons -Repository PSGallery

# Set-Theme
oh-my-posh init pwsh --config "$env:POSH_THEMES_PATH/slim.omp.json" | Invoke-Expression # Winget install JanDeDobbeleer.OhMyPosh


# z commands to jump to directories
# Invoke-Expression (& { (zoxide init powershell | Out-String) }) #winget install ajeetdsouza.zoxide

# Import-Module PSReadLine # Install-Module PSReadLine
# Set-PSReadLineKeyHandler -Key Shift+Tab -Function Complete

# Scripts in here
. "C:\wc\code\PS-Scripts.ps1"
# Variable in here
. "C:\wc\code\PS-Variables.ps1"