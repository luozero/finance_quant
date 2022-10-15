#!/bin/bash

base=$(cd $(dirname ${BASH_SOURCE:-$0});pwd)
cd ${base}

echo '-----------begin all process-----------'

cfg=./conf/conf_release.json
python3 data_download.py -f ${cfg}
python3 factors_calc.py -f ${cfg}
python3 factors_analysis.py -f ${cfg}

echo '-----------finished all process-----------'
