# Pulled from $PROFILE

function chkfont(){ # Returns all the fonts installed on the system
    return (New-Object System.Drawing.Text.InstalledFontCollection).Families
}

function Show-Path-Env(){
    return $env:Path -replace ';', "`n"
}
