#!/usr/bin/env python3
import json, time

OUTPUT_MD_FILENAME = "xr17032.md"
OUTPUT_PDF_FILENAME = "xr17032.pdf"
PAGEBREAK = "<div style='page-break-after: always;'></div>"

result = ""

current_date_str = time.strftime("%B %-d, %Y")

draft_number_str = "" 
if True:
#try:
	draft_number_file = open("draft_number", "r")
	draft_number_str = draft_number_file.read()
	draft_number_file.close()
	draft_number_file = open("draft_number", "w")
	draft_number = int(draft_number_str) + 1
	draft_number_str = str(draft_number)
	draft_number_file.write(draft_number_str)
	draft_number_file.close()
#except:
#	print("draft number file open/read/write exception")

license_str = ""
try:
	license_file = open("LICENSE")
	license_str = license_file.read()
	license_file.close()
except:
	print("license file open/read exception")

result += f"""
---
title: XR/17032 Processor Specification
date: {current_date_str}
subtitle: Draft {draft_number_str}

---

{PAGEBREAK}
# SPECIFICATION COPYRIGHT
{license_str}
{PAGEBREAK}

TODO:

 - code to organize chapter section .json files into the markdown
 - create more section .json files

"""

# todo chapters

try:
	md_file = open("docs/" + OUTPUT_MD_FILENAME, "w")
	md_file.write(result)
	md_file.close()
except:
	print("markdown file write exception")
