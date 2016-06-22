#! /bin/bash

cut -f1 | 
sed 's/$/\n/' |
tr ' ' '\n' |
sed 's/^..*/& : &/' |
./extract_features.py |
./unlabel.sh