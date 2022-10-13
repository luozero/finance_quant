#!/bin/bash

base=$(cd $(dirname ${BASH_SOURCE:-$0});pwd)
cd ${base}

echo '-----------begin all process-----------'

python3 factors_calc.py -f conf_index.json
python3 factors_analysis.py -f conf_index.json

python3 factors_calc.py -f conf_stock.json
python3 factors_analysis.py -f conf_stock.json

echo '-----------finished all process-----------'
