#!/bin/bash

python_file_path=$1
ruff_config_path=$2

ruff check $python_file_path --statistics --output-format=json --config $ruff_config_path