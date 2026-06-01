#!/bin/python3

__copyright__   = "Copyright 2026, VISA Lab"
__license__     = "MIT"

"""
File: autograder.py
Author: Siddharth Jain
"""

import os
import sys
import pdb
import glob
import shutil
import zipfile
import logging
import subprocess
import pandas as pd
import importlib.util

from utils import *
from grade_project2 import *

parser = argparse.ArgumentParser(description='Project path')
parser.add_argument('--project_path', type=str, help='Path to the test scripts')
parser.add_argument('--mode', type=str, required=False, choices=['start', 'resume'], help='grading mode', default='start')

args            = parser.parse_args()
project_path    = args.project_path
arg_mode        = args.mode

grade_project           = "Project-2"
roster_csv              = 'class_roster.csv'
grader_results_csv      = f'Project-2-grades.csv'
zip_folder_path         = f'submissions/'
test_module_script      = f'{os.getcwd()}/test_module.sh'
total_num_test_cases    = 3
resume_test_case        = 1
# (test case, producers, consumers, buffer size, regular processes, zombie processes, dmesg-log points)
test_cases              = [(1, 0, 5, 5, 0, 10, 20), (2, 1, 10, 5, 0, 10, 20), (3, 1, 20, 10, 50, 50, 30),]

log_file = 'autograder.log'
logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
        )
logger = logging.getLogger()

print_and_log(logger, f'+++++++++++++++++++++++++++++++ CSE330 Autograder  +++++++++++++++++++++++++++++++')
print_and_log(logger, "- 1) The script will first look up for the zip file following the naming conventions as per project document")
print_and_log(logger, "- 2) The script will then do a sanity check on the zip file to make sure all the expected files are present")
print_and_log(logger, "- 3) Execute the test cases as per the Grading Rubrics")
print_and_log(logger, "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

print_and_log(logger, f'++++++++++++++++++++++++++++ Autograder Configurations ++++++++++++++++++++++++++++')
print_and_log(logger, f"Project Path: {project_path}")
print_and_log(logger, f"Grade Project: {grade_project}")
print_and_log(logger, f"Class Roster: {roster_csv}")
print_and_log(logger, f"Zip folder path: {zip_folder_path}")
print_and_log(logger, "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

roster_df 	     = pd.read_csv(roster_csv)
restart_required = False
err_at_tc        = 0

if args.mode == 'resume':
	# If mode is 'resume', find the last row of the file
	total_graded_students, resume_test_case, grades_df, previous_grade_points, previous_grade_comments = reload_graded_results(logger, grader_results_csv, "resume", total_num_test_cases)
else:
	#Create a blank grades csv
	grades_df = create_dummy_results_csv(logger, roster_df, grader_results_csv, total_num_test_cases)

for index, row in roster_df.iterrows():

    first_name  = row['First Name']
    last_name   = row['Last Name']
    name        = f"{row['Last Name']} {row['First Name']}"
    asuid       = row['ASUID']

    if args.mode == 'resume' and index < total_graded_students:
        continue

    print_and_log(logger, f'++++++++++++++++++ Grading for {last_name} {first_name} ASUID: {asuid} +++++++++++++++++++++')
    restart_required    = False
    grade_points 	    = 0
    grade_comments 	    = ""
    pattern 		    = os.path.join(zip_folder_path, f'*-{asuid}*.zip')
    zip_files 		    = glob.glob(pattern)

    if args.mode == 'resume':
        if previous_grade_points:
            grade_points            = previous_grade_points
            previous_grade_points   = 0
        else:
            grade_points = 0
        if previous_grade_comments:
            grade_comments          = previous_grade_comments
            previous_grade_comments = ""
        else:
            grade_comments = ""

    if zip_files and os.path.isfile(zip_files[0]):

        zip_file 	= zip_files[0]
        sanity_pass = False

        extracted_folder = f'extracted'
        del_directory(logger, extracted_folder)
        extract_zip(logger, zip_file, extracted_folder)

        grades_df.loc[grades_df['ASUID'] == asuid, 'Submission-Found'] = "Pass"

        prod_cons_exits     = glob.glob("extracted/source_code/producer_consumer.c")
        km_makefile         = glob.glob("extracted/source_code/Makefile")
        unwanted_files      = check_unwanted_files(logger, extracted_folder)

        if prod_cons_exits and km_makefile:
            sanity_pass     = True
            sanity_status   = "Pass"
            sanity_comments = "Unzip submission and check folders/files: PASS. Enough files found to proceed with grading."
        else:
            sanity_pass     = False
            sanity_status   = "Fail"
            sanity_comments = f"Unzip submission and check folders/files: FAIL. All expected files not found. Please check if the zip follows the correct structure as per the project document."

        grade_comments  += sanity_comments
        grades_df.loc[grades_df['ASUID'] == asuid, 'Sanity-Test'] = sanity_status
        grades_df.loc[grades_df['ASUID'] == asuid, 'Sanity-logs'] = sanity_comments
        grades_df.loc[grades_df['ASUID'] == asuid, 'Zip-logs']    = sanity_comments

        if sanity_pass:
            test_results = {}

            cse330_grader  = grader_project2(logger, asuid)

            for num, prod, cons, size, regular, zombies, dmesg_points in test_cases:
                # Skip to the appropriate test case in resume mode.
                if args.mode == 'resume' and num < resume_test_case:
                    continue

                grades_df.loc[grades_df['ASUID'] == asuid, 'Grading-Status'] = "In-Progress"
                res = {}
                restart_required = False

                restart_required, result    = cse330_grader.execute_kernel_module(asuid, extracted_folder, test_module_script, num, prod, cons, size, regular, zombies, dmesg_points)
                res[f'tc_{num}'] = result

                update_test_case_result(grades_df, asuid, num, res)
                test_results[f"tc_{num}"]   = result
                grade_comments              += result[1] + "\n"
                grades_df.to_csv(grader_results_csv, mode='w', header=True, index=False)

                if restart_required:
                    err_at_tc = num
                    break

            #grade_points = sum(result[0] for result in test_results.values())
            grade_points = sum(float(val[2]) for val in test_results.values()  if isinstance(val, list) and len(val) > 2 and isinstance(val[2], (int, float)))
            if grade_points == 99.99: grade_points = 100

            penalty_message = ""
            if unwanted_files:
                # -5 pts for files outside the expected submission structure
                grade_points   -= 5
                file_list       = ", ".join(unwanted_files[:10])
                if len(unwanted_files) > 10:
                    file_list += f", and {len(unwanted_files) - 10} more"
                message         = f"[Grade-Penalty] Points deducted: 5. Unwanted file(s) found: {file_list}."
                penalty_message = message
                grade_comments += "\n" + message
                print_and_log(logger, message)

            if grade_points < 0: grade_points = 0
            if penalty_message:
                final_message = f"Final Grade Points: {grade_points}"
                grade_comments += "\n" + final_message
                existing_comments = grades_df.loc[grades_df['ASUID'] == asuid, "Comments"].astype(str)
                grades_df.loc[grades_df['ASUID'] == asuid, "Comments"] = existing_comments + "\n" + penalty_message + "\n" + final_message
            print_and_log(logger, "--------------------------------------------------------")
            print_and_log(logger, f"Total Grade Points: {grade_points}")
            print_and_log(logger, "--------------------------------------------------------")
            test_results["grade_points"] = grade_points
            grades_df.loc[grades_df['ASUID'] == asuid, "grade_points"] = grade_points
            grades_df.loc[grades_df['ASUID'] == asuid, "Total grades"] = grade_points
            grades_df.loc[grades_df['ASUID'] == asuid, 'Grading-Status'] = "Done"

            del_directory(logger, extracted_folder)
        else:
            for idx, num in enumerate(range(1, total_num_test_cases + 1)):
                results={}
                results[f'tc_{num}'] = ["Failed", sanity_comments, 0, sanity_comments]
                update_test_case_result(grades_df, asuid, num, results)
                grades_df.loc[grades_df['ASUID'] == asuid, "grade_points"] = 0

            grades_df.loc[grades_df['ASUID'] == asuid, 'Grading-Status'] = "Done"
            grade_comments += sanity_comments
            del_directory(logger, extracted_folder)

    else:
        sanity_pass     = False
        sanity_status   = "Fail"
        sanity_comments  = f"Submission File (.zip) not found for {asuid}."
        print_and_log_error(logger, sanity_comments)
        grade_comments      	+= f"{sanity_comments} There is a possiblity that student has either misspelled their asuid or student did not submit the assignment. Kindly validate manually."
        print_and_log_error(logger, f"{sanity_comments} There is a possiblity that student has either misspelled their asuid or student did not submit the assignment. Kindly validate manually.")

        grades_df.loc[grades_df['ASUID'] == asuid, 'Submission-Found']  = sanity_status
        grades_df.loc[grades_df['ASUID'] == asuid, 'Zip-logs']          = sanity_comments
        grades_df.loc[grades_df['ASUID'] == asuid, 'Sanity-logs']       = sanity_comments
        grades_df.loc[grades_df['ASUID'] == asuid, 'Sanity-Test']       = sanity_status
        grades_df.loc[grades_df['ASUID'] == asuid, 'Grading-Status']    = "Done"

        for idx, num in enumerate(range(1, total_num_test_cases + 1)):
            results={}
            results[f'tc_{num}'] = ["Failed", sanity_comments, 0, grade_comments]
            update_test_case_result(grades_df, asuid, num, results)

        grades_df.loc[grades_df['ASUID'] == asuid, "grade_points"] = 0

    if restart_required:
        print_and_log (logger, f'!!!!!!! WARNING !!!!!! : Error encountered while grading for student {last_name} {first_name}. Please reboot your vm and rerun the autograder in resume mode')
        print_and_log(logger, "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        if err_at_tc == total_num_test_cases:
            grades_df.loc[grades_df['ASUID'] == asuid, 'Grading-Status']    = "Done"

        grades_df.to_csv(grader_results_csv, mode='w', header=True, index=False)
        break
    else:
        grades_df.to_csv(grader_results_csv, mode='w', header=True, index=False)

    print_and_log(logger, f"Grading completed for {last_name} {first_name} ASUID: {asuid}")
    print_and_log(logger, "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    logger.handlers[0].flush()

print_and_log(logger, f"Grading complete for {grade_project}. Check the {grader_results_csv} file.")
