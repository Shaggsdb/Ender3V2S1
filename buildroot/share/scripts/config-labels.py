#!/usr/bin/env python3
#
# for python3.5 or higher
#-----------------------------------
# Within Marlin project MarlinFirmware/Configurations, this program visits all folders
# under .../config/examples/*, processing each Configuration.h, Configuration_adv.h,
# _Bootscreen.h, and _Statusscreen.h, to insert:
#    #define CONFIG_EXAMPLES_DIR "examples/<style>/<vendor>/<model>"
# ... or similar path leading to this file.
#
# Warning: The program modifies files in place, so be sure to back them up first if needed.
# Can be run multiple times if needed. Only modifies files which don't have
# correct #define CONFIG_EXAMPLES_DIR line.
#
# Invocation:
#-------------
# 1. Change directory to your MarlinFirmware/Configurations working copy
# 2. python3 config-labels.py
#
#-----------------------------------
# 2020-05-10 GMW original
# 2020-06-05 SRL style tweaks
#-----------------------------------
#
<<<<<<< HEAD
import sys
=======
import sys,os
>>>>>>> af308590f4efa68068226d4f6b05924d56f02436
from pathlib import Path
from distutils.dir_util import copy_tree  # for copy_tree, because shutil.copytree can't handle existing files, dirs

# Modify input_examples_dir and output_examples_dir for your installation
# No trailing slash
# Setting output_examples_dir = input_examples_dir causes the program to insert into the existing files.

input_examples_dir = r'config/examples'
# output_examples_dir   = input_examples_dir
output_examples_dir = r'config/examples'

#-------------------------------------

files_to_mod = ['Configuration.h', 'Configuration_adv.h', '_Bootscreen.h', '_Statusscreen.h']

macro_name     = 'CONFIG_EXAMPLES_DIR'
def_macro_name = '#define ' + macro_name

filenum = 0
different_out_dir = not (output_examples_dir == input_examples_dir)

#----------------------------------------------
def process_file(subdir: str, filename: str):
#----------------------------------------------
	global filenum
	filenum += 1

	print(str(filenum) + '  ' + filename + ':  ' + subdir)

	def_line = (def_macro_name + ' "'  + subdir.replace('\\', '/')  + '"')

	#------------------------
	# Read file
	#------------------------
	lines = []
<<<<<<< HEAD
	infilepath = Path(input_examples_dir, subdir, filename)
	try:
		# UTF-8 because some files contain unicode chars
		with infilepath.open('rt', encoding="utf-8") as infile:
=======
	infilepath = os.path.join(input_examples_dir, subdir, filename)
	try:
		# UTF-8 because some files contain unicode chars
		with open(infilepath, 'rt', encoding="utf-8") as infile:
>>>>>>> af308590f4efa68068226d4f6b05924d56f02436
			lines = infile.readlines()

	except Exception as e:
		print('Failed to read file: ' + str(e) )
		raise Exception

	lines = [line.rstrip('\r\n') for line in lines]

	#------------------------
	# Process lines
	#------------------------
	file_modified    = False

	# region state machine
	# -1 = before pragma once;
	# 0 = region to place define;
	# 1 = past region to place define
	region      = -1

	outlines = []
	for line in lines:
		outline = line

		if (region == -1) and (def_macro_name in line):
			outline       = None
			file_modified = True

		elif (region == -1) and ('pragma once' in line):
			region = 0

		elif (region == 0):
			if (line.strip() == ''):
				pass
			elif (def_macro_name in line):
				region = 1
				if line == def_line:   # leave it as is
					pass
				else:
					outline       = def_line
					file_modified = True
			else: # some other string
				outlines.append(def_line)
				outlines.append('')
				region = 1
				file_modified = True

		elif (region == 1):
			if (def_macro_name in line):
				outline       = None
				file_modified = True
			else:
				pass

		# end if
		if outline is not None:
			outlines.append(outline)
	# end for

	#-------------------------
	#     Output file
	#-------------------------
<<<<<<< HEAD
	outdir      = Path(output_examples_dir, subdir)
	outfilepath = outdir / filename
=======
	outdir      = os.path.join(output_examples_dir, subdir)
	outfilepath = os.path.join(outdir, filename)
>>>>>>> af308590f4efa68068226d4f6b05924d56f02436

	if file_modified:
		# Note: no need to create output dirs, as the initial copy_tree
		# will do that.

<<<<<<< HEAD
		print('  writing ' + outfilepath)
		try:
			# Preserve unicode chars; Avoid CR-LF on Windows.
			with outfilepath.open("w", encoding="utf-8", newline='\n') as outfile:
				outfile.write("\n".join(outlines) + "\n")
=======
		print('  writing ' + str(outfilepath))
		try:
			# Preserve unicode chars; Avoid CR-LF on Windows.
			with open(outfilepath, "w", encoding="utf-8", newline='\n') as outfile:
				outfile.write("\n".join(outlines))
				outfile.write("\n")
>>>>>>> af308590f4efa68068226d4f6b05924d56f02436

		except Exception as e:
			print('Failed to write file: ' + str(e) )
			raise Exception
	else:
<<<<<<< HEAD
		print('  no change for ' + outfilepath)
=======
		print('  no change for ' + str(outfilepath))
>>>>>>> af308590f4efa68068226d4f6b05924d56f02436

#----------
def main():
#----------
	global filenum
	global input_examples_dir
	global output_examples_dir
	filenum = 0

	#--------------------------------
	# Check for requirements
	#--------------------------------
	input_examples_dir  = input_examples_dir.strip()
	input_examples_dir  = input_examples_dir.rstrip('\\/')
	output_examples_dir = output_examples_dir.strip()
	output_examples_dir = output_examples_dir.rstrip('\\/')

<<<<<<< HEAD
	for dir in (input_examples_dir, output_examples_dir):
		if not Path(dir).exists():
=======
	for dir in [input_examples_dir, output_examples_dir]:
		if not (os.path.exists(dir)):
>>>>>>> af308590f4efa68068226d4f6b05924d56f02436
			print('Directory not found: ' + dir)
			sys.exit(1)

	#--------------------------------
	# Copy tree if necessary.
	#--------------------------------
	# This includes files that are not otherwise included in the
	# insertion of the define statement.
	#
	if different_out_dir:
		print('Copying files to new directory: ' + output_examples_dir)
		try:
			copy_tree(input_examples_dir, output_examples_dir)
		except Exception as e:
			print('Failed to copy directory: ' + str(e) )
			raise Exception

	#-----------------------------
	# Find and process files
	#-----------------------------
<<<<<<< HEAD
	len_input_examples_dir = 1 + len(input_examples_dir)
=======
	len_input_examples_dir = len(input_examples_dir);
	len_input_examples_dir += 1
>>>>>>> af308590f4efa68068226d4f6b05924d56f02436

	for filename in files_to_mod:
		input_path = Path(input_examples_dir)
		filepathlist = input_path.rglob(filename)

		for filepath in filepathlist:
			fulldirpath = str(filepath.parent)
			subdir      = fulldirpath[len_input_examples_dir:]

			process_file(subdir, filename)

#==============
print('--- Starting config-labels ---')
main()
print('--- Done ---')
