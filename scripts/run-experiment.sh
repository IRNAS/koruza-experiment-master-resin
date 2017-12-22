#!/bin/bash -e

work_dir=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

echo "Running all KORUZA experiment monitoring scripts."
nohup python ${work_dir}/link-test.py > /data/koruza-link-test.log &
nohup python ${work_dir}/weather.py > /data/koruza-weather.log &
wait
