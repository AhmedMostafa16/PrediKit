#!/bin/sh

PROG=`basename $0`

echo $PROG "Installing dependencies:"
pip install -r requirements.txt

echo $PROG : "Completed normally"
exit 0
