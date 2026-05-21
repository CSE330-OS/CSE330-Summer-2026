# Autograder for Project 1

Make sure that you use the provided autograder and follow the instructions below to test your project submission. Failure to do so may cause you to lose all the project points and there will be absolutely no second chance.

- Download the zip file you submitted from Canvas. 
- Download the autograder from GitHub: `https://github.com/CSE330-OS/CSE330-Summer-2026.git`
  - In order to clone the GitHub repository follow the below steps:
  - `git clone https://github.com/CSE330-OS/CSE330-Summer-2026.git`
  - `cd CSE330-Summer-2026/`
  - `git checkout project-1`
- Create a directory `submissions` in the CSE330-Summer-2026 directory and move your zip file to the submissions directory.

## Prepare to run the autograder
- Install all the dependencies using the provided script `install.sh`
- Populate the `class_roster.csv`
 
## Run the autograder
- To run the autograder: 
```
source .venv/bin/activate
python3 autograder.py
```
- The autograder will look for submissions for each entry present in the class_roster.csv
- For each submission the autograder:
  - Extracts the required files from the submission and parses the entries.
  - Test the project as per the grading rubrics and allocate grade points.
    
## Sample Output

```
(.venv) linustorvalds@cse330:~/CSE330-Summer-2026$ python3 autograder.py 
+++++++++++++++++++++++++++++++ CSE330 Autograder  +++++++++++++++++++++++++++++++
- 1) The script will first look up for the zip file following the naming conventions as per project document
- 2) The script will then do a sanity check on the zip file to make sure all the expected files are present
- 3) Execute the test cases as per the Grading Rubrics
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++ Autograder Configurations ++++++++++++++++++++++++++++
Grade Project: Project-1
Class Roster: class_roster.csv
Zip folder path: submissions/
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++ Grading for Torvalds Linus ASUID: 1225754101 +++++++++++++++++++++
Submission file: submissions/project-1-1225754101.zip unzipped to folder: extracted
[Sanity check] File found: extracted/module/my_module.c
[Sanity check] File found: extracted/module/Makefile
[Sanity check] File found: extracted/syscall/my_syscall.c
[Sanity check] File found: extracted/syscall/Makefile
[Sanity check] File found: extracted/userspace/syscall_in_userspace_test.c
[Sanity check] File found: extracted/screenshot/syscall_output.png
[Sanity check] File found: extracted/screenshot/uname.png
[Sanity check] File found: extracted/screenshot/lsb_release.png
[Sanity check] No unwanted files found.
Sanity Test Passed: Enough files found to proceed with grading.
----------------- Executing Test-Case:1 ----------------
[TC-1-log] Pass
[TC-1-log] lsb_release desired output found.
[TC-1-log] Linustorvaldscse330: lsb_release a No LSB modules are available. Distributor ID: Ubuntu Description: Ubuntu 26.04 LTS Release: 26.04 Codename: resolute Linustorvaldscse330: fj
[TC-1-log] Points deducted: 0
----------------- Executing Test-Case:2 ----------------
[TC-2-log] Pass
[TC-2-log] uname desired output found.
[TC-2-log] linustorvaldscse330: uname a Linux cse330 7.0.9CSE330Summer226LinusTorvalds 1 SMP PREEMPT_DYNAMIC Mon May 18 5:13:38 UTC 2026 aarch64 GNULinux Linustorvaldscse330: fj
[TC-2-log] Points deducted: 0
----------------- Executing Test-Case:3 ----------------
[TC-3-log] Extracted text: Linustorvaldscse330:userspace gcc o syscall_in_userspace syscall_in_userspace_test.c Linustorvaldscse330:userspace .syscall_in_userspace Linustorvaldscse330:userspace sudo dmesg tail n 1 217.673993 This is the new system call Linus Torvalds implemented. linustorvaldscse330:userspace j
Pass
[TC-3-log] syscall_output correct.
[TC-3-log] Points deducted: 0
----------------- Executing Test-Case:4 ----------------
[TC-4-log] Kernel module test passed. Unzipping to "unzip_1779336241"
[TC-4-log]: Look for module directory
[log]: - directory /home/linustorvalds/Project-1/autograder/unzip_1779336241/module found
[TC-4-log]: Look for Makefile
[log]: - file /home/linustorvalds/Project-1/autograder/unzip_1779336241/module/Makefile found
[TC-4-log]: Look for source file (my_module.c)
[log]: - file /home/linustorvalds/Project-1/autograder/unzip_1779336241/module/my_module.c found
[TC-4-log]: Compile the kernel module
[log]: - Compiled successfully
[TC-4-log]: Load the kernel module
[TC-4-log]: - Loaded successfully
[TC-4-log]: Check dmesg output
[TC-4-log]: - Output is correct
[TC-4-log]: Unload the kernel module
[TC-4-log]: - Kernel module unloaded successfully
[my_module]: Passed with 25 out of 25
[Total Score]: 25 out of 25

[TC-4-log] Points deducted:0
--------------------------------------------------------
Total Grade Points: 100
--------------------------------------------------------
Removed extracted folder: extracted
Grading completed for Torvalds Linus ASUID: 1225754101
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Grading complete for Project-1. Check the Project-1-grades.csv file.
(.venv) linustorvalds@cse330:~/CSE330-Summer-2026$ 
```
