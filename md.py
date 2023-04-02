#!/usr/bin/env python3.11
import time
import tomllib
import os


OUTPUT_MD_FILENAME = "xr17032.md"
OUTPUT_TXT_FILENAME = "xr17032.txt"

PAGEBREAK = "\\pagebreak"
PAGEBREAK_MD = "<div style='page-break-after: always;'></div>"

result = ""

current_date_str = time.strftime("%B %-d, %Y")

draft_number_str = "-1" 
try:
	draft_number_file = open("draft_number", "r")
	draft_number_str = draft_number_file.read()
	draft_number_file.close()
except:
	print("ERROR: draft number file open/read exception")
try:
	draft_number_file = open("draft_number", "w")
except:
	print("ERROR: draft number file open exception")
draft_number = int(draft_number_str) + 1
if draft_number == 0:
	print("ERROR: draft number error")
draft_number_str = str(draft_number)
try:
	draft_number_file.write(draft_number_str)
	draft_number_file.close()
except:
	print("ERROR: draft number file write exception")

license_str = ""
try:
	license_file = open("LICENSE")
	license_str = license_file.read()
	license_file.close()
except:
	print("ERROR: license file open/read exception")

header_includes = """| 
	\\rowcolors{2}{gray!0}{gray!10}
	\\usepackage{fancyhdr}
	\\pagestyle{fancy}
"""

result += f"""
---
title: XR/17032 Processor Specification

date: {current_date_str}

subtitle: Draft {draft_number_str}

classoption: table

header-includes: {header_includes}

---

{PAGEBREAK}

# SPECIFICATION COPYRIGHT

&nbsp;  

{license_str}

"""

try:
	chapters_file = open("src/chapters.toml")
	chapters_str = chapters_file.read()
	chapters_file.close()
except:
	print("ERROR: chapters file open/read exception")

chapters_data = tomllib.loads(chapters_str)

for chapter in chapters_data["chapters"]:
	result += f"{PAGEBREAK}\n\n"
	result += f"# {chapter.upper()}\n\n&nbsp;  \n\n"

	if chapter not in os.listdir("src/"):
		print(f"ERROR: {chapter} chapter directory not found")
		continue

	for filename in sorted(os.listdir("src/" + chapter)):
		if ".toml" not in filename:
			continue

		f_str = ""
		try:
			f = open("src/" + chapter + "/" + filename)
			f_str = f.read()
			f.close()
		except:
			print("ERROR: " + chapter + "/" + filename, "open/read exception")

		f_data = tomllib.loads(f_str)

		if chapter == "opcodes":
			should_skip_opcode = False
			# opcode toml formatting check: opcode files must conform for consistency.
			for key in ["name", "mnemonic", "encoding", "text", "implementation"]:
				if key not in f_data:
					print(f"ERROR: '{key}' key missing from opcode file {filename}")
					should_skip_opcode = True
			if should_skip_opcode:
				continue

			name = f_data["name"]
			mnemonic = f_data["mnemonic"]
			encoding = f_data["encoding"]
			text = f_data["text"]
			implementation = f_data["implementation"]
			notes = ""
			if "notes" in f_data:
				notes = f_data["notes"]

			result += f"## {name} - {mnemonic}\n\n&nbsp;  \n\n"

			result += "### Encoding\n\n"


			encoding_bits_total	= len(encoding)

			current_encoding_bit = encoding_bits_total - 1
			current_encoding_index = 0

			encoding_sections = []

			c = encoding[0]
			start_c = c

			ENCODING_STATE_DIGIT = 1
			ENCODING_STATE_LETTER = 2

			if c.isdigit():
				encoding_state = ENCODING_STATE_DIGIT
			else:
				encoding_state = ENCODING_STATE_LETTER

			section = { "bit_end": current_encoding_bit,
						"bit_start": -1,
						"text": "" }

			for c in encoding:
				if encoding_state == ENCODING_STATE_DIGIT:
					if c.isdigit(): # process digit into current section
						section["text"] += c
					else: # change states, chop section make new section put into sections
						encoding_state = ENCODING_STATE_LETTER
						section["bit_start"] = current_encoding_bit + 1
						encoding_sections.append(section)
						section = { "bit_end": current_encoding_bit,
									"bit_start": -1,
									"text": c }
						start_c = c
				elif encoding_state == ENCODING_STATE_LETTER:
					if not c.isdigit() and c == start_c: # process letter into current section
						section["text"] += c
					else: # change states, chop section make new section put into sections
						if c.isdigit():
							encoding_state = ENCODING_STATE_DIGIT
						else: # is letter and c != start_c
							encoding_state = ENCODING_STATE_LETTER
						section["bit_start"] = current_encoding_bit + 1
						encoding_sections.append(section)
						section = { "bit_end": current_encoding_bit,
									"bit_start": -1,
									"text": c }
						start_c = c
				current_encoding_index += 1
				current_encoding_bit -= 1

			if section["text"] != "":
				section["bit_start"] = 0
				encoding_sections.append(section)

			for section in encoding_sections:
				result += f"| [{section['bit_end']}:{section['bit_start']}] "
			result += "|\n"
			for section in encoding_sections:
				result += "| :-: "
			result += "|\n"
			for section in encoding_sections:
				result += f"| `{section['text']}`"
			result += "|\n\n"


			result += "### Description\n\n"
			result += f"{text}\n\n&nbsp;  \n\n"
			
			result += "### Implementation\n\n"
			result += f"```\n{implementation}\n```\n\n"
			
			if notes != "":
				result += "### Notes\n\n\n"
				result += f"{notes}\n\n"

			result += f"{PAGEBREAK}\n\n"


		else:			
			if "text" in f_data:
				result += f_data["text"]

		result += "&nbsp;  \n\n"

# write result files
try:
	txt_file = open("docs/" + OUTPUT_TXT_FILENAME, "w")
	txt_file.write(result)
	txt_file.close()
except:
	print("ERROR: txt file write exception")

result = result.replace(PAGEBREAK, PAGEBREAK_MD)

try:
	md_file = open("docs/" + OUTPUT_MD_FILENAME, "w")
	md_file.write(result)
	md_file.close()
except:
	print("ERROR: markdown file write exception")

