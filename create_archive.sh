#!/bin/bash

# This script creates the 'temoa.py' zip archive/executable.  I do not know if
# it is portable, but I know that it correctly creates the executable with the
# Ubuntu Linux distribution's version of Zip, Info-ZIP.

# To create the archive, execute with no arguments (in this directory), or
# with '--save'.  The save argument merely saves the temporary zip file from
# which 'temoa.py' is created.

set -e

CLEANUP=true

PKG_NAME=temoa.py
PKG_PATH=./temoa_model

if [[ "$1" = "--save" ]]; then
	CLEANUP=false
fi

(
	cd "$PKG_PATH"
	find . -name "*.py" -print | zip "../$PKG_PATH.zip" -q@ --symlinks
)

echo "#!/usr/bin/env coopr_python" > "$PKG_NAME"
cat temoa_model.zip >> "$PKG_NAME"
chmod 755 "$PKG_NAME"

if [[ "true" = "$CLEANUP" ]]; then
	\rm -f "$PKG_PATH.zip"
fi
