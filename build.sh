#!/usr/bin/bash

python3 md.py
pandoc docs/xr17032.md -t html -o docs/xr17032.pdf
