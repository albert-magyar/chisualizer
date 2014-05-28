#!/bin/bash

python main.py -e "../../flo/emulator/fix-console" -a :filename ../tests/gcd/GCD.hex :use-chisel-api true -d "../tests/gcd/gcd.xml" --log_level debug
