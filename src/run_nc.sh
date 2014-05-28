#!/bin/bash

# run_nc IP port layout_file

python main.py -e "nc $1 $2" -d "$3" --log_level debug
