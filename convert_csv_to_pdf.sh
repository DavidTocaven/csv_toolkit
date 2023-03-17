#!/bin/bash
# convert all csv files into pdfs
if [$1 -eq 0 ]
then
	soffice --headless --convert-to pdf *.csv
else
	soffice --headless --convert-to pdf "$1.csv"
fi
