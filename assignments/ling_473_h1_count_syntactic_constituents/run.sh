#!/bin/bash
##### Constants
TITLE="LING 473 Project 1 Execution script"
RIGHT_NOW=$(date +"%x %r %Z")
TIME_STAMP="Updated on $RIGHT_NOW by $USER"
PY_ENV="/opt/python-3.4.1/bin/python3.4"
##################### Functions
echo ${TITLE}
echo ${RIGHT_NOW} 
function runCountConstituents()
{ 
${PY_ENV} ./countConstituents.py
}
runCountConstituents