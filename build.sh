#!/usr/bin/bash

python3.11 md.py
pandoc docs/xr17032.txt -V geometry:margin=1in --toc -o docs/xr17032.pdf
