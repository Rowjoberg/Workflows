# Pulled from $PROFILE

function Show-Fonts(){
  # Returns all the fonts installed on the system
  return (New-Object System.Drawing.Text.InstalledFontCollection).Families
}
function Test-Script-Help(){
  $tshelp = "When updating the config files, run the following commands:
        progdatabase . # in an updated http://subversion/svn/csm/tools/AmpTest/config
        progression --database .\prog_config.zip # To test the database
    Commit all modified files int the config folder to svn."
  return Write-Output $tshelp
}

function Find-Part-Certs($partnum, $AIRNo="_1", $outputpath="C:\Users\rfromberg\AIRs\"+$partnum+$AIRNo){
  if ($null -eq $partnum){
    Write-Output "Please provide a Syteline part number"
  } else {
    mkdir -path $outputpath  
    Set-Location $outputpath
    C:\wc\find_item_certifications.exe --parts $partnum --outputdir $outputpath
    C:\wc\part_graph.exe --parts $partnum --outputdir $outputpath
    Invoke-Item $outputpath
    Write-Output $outputpath
    return 
  }    
}

function Find-Part-List($listfile, $outputpath="C:\Users\rfromberg\AIRs\List"){
  if ($null -eq $listfile){
    Write-Output "Please provide a list of Syteline numbers"
  } else {
    mkdir -path $outputpath  
    Set-Location $outputpath
    C:\wc\find_item_certifications.exe --file $listfile --outputdir $outputpath
    C:\wc\part_graph.exe --file $listfile --outputdir $outputpath
    Invoke-Item $outputpath
    Write-Output $outputpath
    return 
  }    
}

function AmpTestDevSetup($partnum, $module){
  if ($null -eq $partnum){
    return Write-Output "Please provide a part number"
  }
  if ($null -eq $module){
    return Write-Output "Please provide a module e.g. board, final, etc."
  }
  atdev debug "$partnum-$module"
  Write-Output {Run the following commands:
    .venv\Scripts\activate
    py atdev_main.py # This will run the 'IPM3 Capacitor Bank Test' test script. 
    # atdev --help
  }
}

function Show-Path-Env(){
  return $env:Path -replace ';', "`n"
}

function BOMCompare ($bom1, $bom2){
  if ($null -eq $bom1){
    return Write-Output "Please provide a path to the first BOM"
  }
  if ($null -eq $bom2){
    return Write-Output "Please provide a path to the second BOM"
  }
  # python -m pip install -r "C:\wc\BOM Compare\requirements.txt"
  python "C:\wc\BOM Compare\BOMCompare.py" $bom1 $bom2
    
}

function CertSearch{
  param(
    [string]$Certifications,
    [string]$SearchPath="C:\CSM\CSM\Certifications\",
    [string]$OutputPath="~\AIRs\CertSearch.csv"
  )<#
Usage:
  CertSearch <String: Certificate Number> <Search Path> <Output Path> 

Searches a Path (default="C:\CSM\CSM\Certifications\") for a certification (Filtered by wildcards either side of string), then exports all file paths to a CSV (default="~\AIRs\CertSearch.csv")
#>
  if ($null -eq $Certifications){
    return Write-Output "Please provide a Certification to  search"
  }
  $OutputFiles=(Get-ChildItem -Path $SearchPath -Recurse -Filter *$Certifications* -File | ForEach-Object { $_.FullName })
  $OutputDir=(Get-ChildItem -Path $SearchPath -Recurse -Filter *$Certifications* -Directory | ForEach-Object { $_.FullName })
  return ($OutputFiles > $OutputPath), (Write-Output $OutputDir), (Write-Output "File Locations Written to "$OutputPath), (Invoke-Item $OutputPath)
}
