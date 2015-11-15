#!/bin/bash
#
# Script to clean and build application.
#
rm -r build dist # Removes build files and compiled application.
python setup.py py2app --no-strip # Compiles again.
killall Meta # Kills running application.
./dist/Meta.app/Contents/MacOS/Meta # Calls application binary from the command line.
