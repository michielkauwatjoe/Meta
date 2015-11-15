#!/bin/bash
#
# Script to clean and build application.
#
python setup.py py2app -A # Compile with aliased dependencies
killall Meta # Kills running application.
./dist/Meta.app/Contents/MacOS/Meta # Calls application binary from the command line.
