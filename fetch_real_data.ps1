$ErrorActionPreference = "Stop"
New-Item -ItemType Directory -Force -Path data | Out-Null

Write-Host "Downloading ToeInKAMReduction CSVs (Apache-2.0)..."
Invoke-WebRequest -Uri https://raw.githubusercontent.com/suhlrich/ToeInKAMReduction/main/X_TIdiff.csv -OutFile data/X_TIdiff.csv
Invoke-WebRequest -Uri https://raw.githubusercontent.com/suhlrich/ToeInKAMReduction/main/y_TIP1diff.csv -OutFile data/y_TIP1diff.csv

Write-Host "Downloading UCI Multivariate Gait Data (zip)..."
Invoke-WebRequest -Uri "https://archive.ics.uci.edu/static/public/760/multivariate%2Bgait%2Bdata.zip" -OutFile data/multivariate_gait_data.zip
Expand-Archive -Path data/multivariate_gait_data.zip -DestinationPath data\_gait_tmp -Force
$gait = Get-ChildItem -Path data\_gait_tmp -Recurse -Filter gait.csv | Select-Object -First 1
if ($gait) { Move-Item -Force $gait.FullName data\gait.csv }
Remove-Item -Recurse -Force data\_gait_tmp
Write-Host "Done. Files in .\data\"
