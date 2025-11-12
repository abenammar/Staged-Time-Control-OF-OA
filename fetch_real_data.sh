#!/usr/bin/env bash
set -euo pipefail
mkdir -p data

echo "Downloading ToeInKAMReduction CSVs (Apache-2.0)..."
curl -L -o data/X_TIdiff.csv https://raw.githubusercontent.com/suhlrich/ToeInKAMReduction/main/X_TIdiff.csv
curl -L -o data/y_TIP1diff.csv https://raw.githubusercontent.com/suhlrich/ToeInKAMReduction/main/y_TIP1diff.csv

echo "Downloading UCI Multivariate Gait Data (zip)..."
curl -L -o data/multivariate_gait_data.zip "https://archive.ics.uci.edu/static/public/760/multivariate%2Bgait%2Bdata.zip"
mkdir -p data/_gait_tmp
unzip -o data/multivariate_gait_data.zip -d data/_gait_tmp >/dev/null
# Move gait.csv to data/
if [ -f data/_gait_tmp/gait.csv ]; then
  mv -f data/_gait_tmp/gait.csv data/gait.csv
else
  # sometimes the zip nests the file
  find data/_gait_tmp -name "gait.csv" -exec mv -f {} data/gait.csv \;
fi
rm -rf data/_gait_tmp
echo "Done. Files in ./data/"
