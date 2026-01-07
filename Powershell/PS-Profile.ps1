#=== Script import locations===#
# Add to Powershell $PROFILE  
# Profile in here
#. "~\Workflows\Powershell\PS-Profile.ps1"
# Scripts in here
#. "~\Workflows\Powershell\PS-Scripts.ps1"
# Variable in here
#. "~\Workflows\Powershell\PS-Variables.ps1"

#===Icons in PS===#
Import-Module -Name Terminal-Icons 
#Install-Module -Name Terminal-Icons -Repository PSGallery

#===PSWH Predictive lines===#
# Ensure PSReadLine module is loaded
# Install-Module -Name CompletionPredictor
if (-not (Get-Module -ListAvailable -Name PSReadLine)) {
  Install-PSResource -Name PSReadLine
  Write-Error "PSReadLine module is not installed. Installing it with: Install-PSResource -Name PSReadLine"
  return
}

Import-Module PSReadLine -ErrorAction Stop
Import-Module CompletionPredictor
Set-PSReadLineOption -PredictionSource HistoryAndPlugin
Set-PSReadLineKeyHandler -Chord Tab -Function MenuComplete
Set-PSReadLineKeyHandler -Chord UpArrow -Function HistorySearchBackward
Set-PSReadLineKeyHandler -Chord DownArrow -Function HistorySearchForward
Set-PSReadLineKeyHandler -Chord Shift+Tab -Function AcceptSuggestion
Set-PSReadLineKeyHandler -Chord Ctrl+RightArrow -Function AcceptNextSuggestionWord
Set-PSReadLineOption -PredictionViewStyle ListView
Set-PSReadLineOption -EditMode Windows

#===Excel Functions===#
#Import-Module -Name ImportExcel

#=== Set-Theme===#
oh-my-posh init pwsh --config "~/Workflows/Themes/catppuccinMocha.omp.json" | Invoke-Expression 
# Winget install JanDeDobbeleer.OhMyPosh
 
#=== z commands to jump to directories===#
Invoke-Expression (& { (zoxide init powershell | Out-String) }) 
#winget install ajeetdsouza.zoxide

#=== UV Auto-completions===#
(& uv generate-shell-completion powershell) | Out-String | Invoke-Expression
#===Chocolatey===#
$ChocolateyProfile = "$env:ChocolateyInstall\helpers\chocolateyProfile.psm1"
if (Test-Path($ChocolateyProfile)) {
  Import-Module "$ChocolateyProfile"
}
#===Bat Theme===#
$env:BAT_THEME = 'Catppuccin Mocha'
