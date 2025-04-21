# Add to Powershell $PROFILE  
  # Profile in here
  #. "C:\wc\Workflows\Powershell\PS-Profile.ps1"
  # Scripts in here
  #. "C:\wc\Workflows\Powershell\PS-Scripts.ps1"
  # Variable in here
  #. "C:\wc\Workflows\Powershell\PS-Variables.ps1"

# Import-Module posh-git # Redundant with Oh-My-Posh
# Icons in PS
Import-Module -Name Terminal-Icons #Install-Module -Name Terminal-Icons -Repository PSGallery

# Set-Theme
 oh-my-posh init pwsh --config "C:\wc\Workflows\Themes\Catppuccin_Mocha_2.omp.yaml" | Invoke-Expression # Winget install JanDeDobbeleer.OhMyPosh
 
# z commands to jump to directories
# Invoke-Expression (& { (zoxide init powershell | Out-String) }) #winget install ajeetdsouza.zoxide

Import-Module PSReadLine # Install-Module PSReadLine
Set-PSReadLineKeyHandler -Key Shift+Tab -Function Complete
Set-PSReadLineOption -PredictionSource History
Set-PSReadLineOption -PredictionViewStyle ListView
Set-PSReadLineOption -EditMode Windows

