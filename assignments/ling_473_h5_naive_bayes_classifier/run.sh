#!/bin/bash
##### Constants
TITLE="LING 473 Project 5 Execution script"
RIGHT_NOW=$(date +"%x %r %Z")
TIME_STAMP="Updated on $RIGHT_NOW by $USER"
PY_ENV="/opt/python-3.4.1/bin/python3.4"
PRG_NAME="ling473_pr5.py"
##################### Functions
#echo ${TITLE}
#echo ${RIGHT_NOW} 
function runProgram()
{ 
${PY_ENV} ./${PRG_NAME}
}
runProgram