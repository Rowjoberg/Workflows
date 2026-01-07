# Pulled from $PROFILE
#
# yazi Shell Function
function y {
  $tmp = (New-TemporaryFile).FullName
  yazi $args --cwd-file="$tmp"
  $cwd = Get-Content -Path $tmp -Encoding UTF8
  if (-not [String]::IsNullOrEmpty($cwd) -and $cwd -ne $PWD.Path) {
    Set-Location -LiteralPath (Resolve-Path -LiteralPath $cwd).Path
  }
  Remove-Item -Path $tmp
}
Set-Alias -Name lg -Value lazygit.exe -Description "Lazygit alias for pure gitty greatness"
function Show-Fonts() {
  # Returns all the fonts installed on the system
  return (New-Object System.Drawing.Text.InstalledFontCollection).Families
}
function Test-Script-Help() {
  $tshelp = "When updating the config files, run the following commands:
        progdatabase . # in an updated http://subversion/svn/csm/tools/AmpTest/config
        progression --database .\prog_config.zip # To test the database
    Commit all modified files int the config folder to svn."
  return Write-Output $tshelp
}

function Find-Part-Certs($partnum, $AIRNo="_1", $outputpath="C:\Users\rfromberg\AIRs\"+$partnum+$AIRNo) {
  if ($null -eq $partnum) {
    Write-Output "Please provide a Syteline part number"
  } else {
    mkdir -path $outputpath  
    Set-Location $outputpath
    C:\dev\find_item_certifications.exe --parts $partnum --outputdir $outputpath
    C:\dev\part_graph.exe --parts $partnum --outputdir $outputpath
    Invoke-Item $outputpath
    Write-Output $outputpath
    return 
  }    
}

function Find-Part-List($listfile, $outputpath="C:\Users\rfromberg\AIRs\List") {
  if ($null -eq $listfile) {
    Write-Output "Please provide a list of Syteline numbers"
  } else {
    mkdir -path $outputpath  
    Set-Location $outputpath
    C:\dev\find_item_certifications.exe --file $listfile --outputdir $outputpath
    C:\dev\part_graph.exe --file $listfile --outputdir $outputpath
    Invoke-Item $outputpath
    Write-Output $outputpath
    return 
  }    
}

function AmpTestDevSetup($partnum, $module) {
  if ($null -eq $partnum) {
    return Write-Output "Please provide a part number"
  }
  if ($null -eq $module) {
    return Write-Output "Please provide a module e.g. board, final, etc."
  }
  atdev debug "$partnum-$module"
  Write-Output {Run the following commands:
    .venv\Scripts\activate
    py atdev_main.py # This will run the 'IPM3 Capacitor Bank Test' test script. 
    # atdev --help
  }
}

function Show-Path-Env() {
  return $env:Path -replace ';', "`n"
}

function BOMCompare ($bom1, $bom2) {
  if ($null -eq $bom1) {
    return Write-Output "Please provide a path to the first BOM"
  }
  if ($null -eq $bom2) {
    return Write-Output "Please provide a path to the second BOM"
  }
  # python -m pip install -r "C:\dev\BOM Compare\requirements.txt"
  python "C:\dev\BOM Compare\BOMCompare.py" $bom1 $bom2
    
}

function CertSearch {
  param(
    [string]$Certifications,
    [string]$SearchPath="C:\CSM\CSM\Certifications\",
    [string]$OutputPath="~\AIRs\CertSearch.csv"
  )<#
Usage:
  CertSearch <String: Certificate Number> <Search Path> <Output Path> 

Searches a Path (default="C:\CSM\CSM\Certifications\") for a certification (Filtered by wildcards either side of string), then exports all file paths to a CSV (default="~\AIRs\CertSearch.csv")
#>
  if ($null -eq $Certifications) {
    return Write-Output "Please provide a Certification to  search"
  }
  $OutputFiles=(Get-ChildItem -Path $SearchPath -Recurse -Filter *$Certifications* -File | ForEach-Object { $_.FullName })
  $OutputDir=(Get-ChildItem -Path $SearchPath -Recurse -Filter *$Certifications* -Directory | ForEach-Object { $_.FullName })
  return ($OutputFiles > $OutputPath), (Write-Output $OutputDir), (Write-Output "File Locations Written to "$OutputPath), (Invoke-Item $OutputPath)
}

function ListSearch {
  [CmdletBinding()] # Enables advanced function features, including -Verbose
  param( 
    [string]$SearchListPath, # Define the path to the text file containing search terms
    [string]$ExportPath, # Define the path to a file to write to
    [string]$SearchDirectory = "G:\Quality\Quality Assurance\Repair, Overhaul, RBR Reports" # Define the directory to search in
  )
  
  # Check if the search list file exists
  if (-Not (Test-Path -Path $SearchListPath)) {
    Write-Verbose "Error: Search list file not found at $SearchListPath" 
    exit
  }

  # Read the search terms from the text file
  $SearchTerms = Get-Content -Path $SearchListPath

  # Check if the search terms are not empty
  if (-Not $SearchTerms) {
    Write-Verbose "Error: No search terms found in the file." 
    exit
  }

  # Loop through each search term and search for matching files or directories
  foreach ($Term in $SearchTerms) {
    Write-Verbose "Searching for: $Term" 
    # Search for files and directories matching the term
    $Results = Get-ChildItem -Path $SearchDirectory -Recurse -Filter *$Term* -File -ErrorAction SilentlyContinue

    if ($Results) {
      Write-Verbose "Found the following matches for '$Term':" 
      $Results | ForEach-Object { Write-Verbose $_.FullName }
      $List += "$Results`n"
    } else {
      Write-Verbose "No matches found for '$Term'." 
    }
  }
  ($List > $ExportPath)
  Write-Host "Search Complete, writing results to:`n$ExportPath"
}


function Copy-ObjectsFromFile {
  <#
    .SYNOPSIS
        Copies files or folders listed in a text file to a destination directory.

    .DESCRIPTION
        Reads a text file containing paths (one per line) and copies each existing file or folder
        to the specified destination. Supports verbose output for detailed progress.

    .PARAMETER PathsFile
        The full path to the text file containing source paths (one per line).

    .PARAMETER Destination
        The destination directory where the files/folders will be copied.

    .PARAMETER VerboseOutput
        Switch to enable verbose printing of copy operations.

    .PARAMETER Limit
        Optional. Maximum number of items to copy from the list.

    .EXAMPLE
        Copy-ObjectsFromFile -PathsFile "C:\paths.txt" -Destination "C:\backup" -VerboseOutput -Limit 10
  #>

  param (
    [Parameter(Mandatory = $true)]
    [string]$PathsFile,

    [Parameter(Mandatory = $true)]
    [string]$Destination,

    [switch]$VerboseOutput,

    [int]$Limit
  )

  # Validate input file
  if (-not (Test-Path $PathsFile)) {
    Write-Error "Paths file not found: $PathsFile"
    return
  }

  # Validate destination
  if (-not (Test-Path $Destination)) {
    Write-Host "Destination does not exist. Creating: $Destination"
    New-Item -ItemType Directory -Path $Destination -Force | Out-Null
  }

  # Read paths
  $paths = Get-Content -Path $PathsFile

  # Apply limit if specified
  if ($Limit -gt 0) {
    $paths = $paths | Select-Object -First $Limit
    if ($VerboseOutput) {
      Write-Host "File copy limit of $Limit reached"
    }
  }

  # Process paths
  foreach ($path in $paths) {
    if (Test-Path $path) {
      Copy-Item -Path $path -Destination $Destination -Force
      if ($VerboseOutput) {
        Write-Host "Copied: $path"
      }
    } else {
      Write-Warning "Path not found: $path"
    }
  }
}

function Remove-ExactFilename {
  <#
    .SYNOPSIS
    Removes all files that match the exact filename within the specified directory and its subdirectories.

    .DESCRIPTION
    This function takes a filename as input and recursively searches through the current directory and all child directories.
    If any file matches the exact filename, it will be deleted. Console logging is included to show progress and results.

    .PARAMETER Filename
    The exact name of the file to remove (including extension).

    .EXAMPLE
    Remove-ExactFilename -Filename "example.txt"
    # Removes all files named 'example.txt' in the current directory and subdirectories.
    #>

  [CmdletBinding()]
  param (
    [Parameter(Mandatory = $true)]
    [string]$Filename
  )

  Write-Host "Starting search for files named '$Filename'..." -ForegroundColor Cyan

  # Get all matching files recursively
  $files = Get-ChildItem -Path . -Recurse -File | Where-Object { $_.Name -eq $Filename }

  if ($files.Count -eq 0) {
    Write-Host "No files found matching '$Filename'." -ForegroundColor Yellow
    return
  }

  Write-Host "Found $($files.Count) file(s) matching '$Filename'." -ForegroundColor Green

  foreach ($file in $files) {
    try {
      Remove-Item -Path $file.FullName -Force
      Write-Host "Removed: $($file.FullName)" -ForegroundColor Magenta
    } catch {
      Write-Host "Failed to remove: $($file.FullName). Error: $($_.Exception.Message)" -ForegroundColor Red
    }
  }

  Write-Host "Operation completed." -ForegroundColor Cyan
}
