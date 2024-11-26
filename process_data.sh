#!/bin/bash

python tools/process_data.py --config configs/ruff_check/python-ruff-filter-refine.yaml > process.log 2>&1 &