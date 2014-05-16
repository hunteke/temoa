#!/bin/bash

# Temoa - Tools for Energy Model Optimization and Analysis
#   linear optimization; least cost; dynamic system visualization
#
# Copyright (C) 2011-2014  Kevin Hunter, Joseph DeCarolis
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU Affero General Public License for more details.
#
# Developers of this script will check out a complete copy of the GNU Affero
# General Public License in the file COPYING.txt.  Users uncompressing this from
# an archive may not have received this license file.  If not, see
# <http://www.gnu.org/licenses/>.


# This script creates the 'temoa.py' zip archive/executable.  I do not know if
# it is portable, but I know that it correctly creates the executable with the
# Ubuntu Linux distribution's version of Zip, Info-ZIP.

# To create the archive, execute with no arguments (in this directory), or
# with '--save'.  The save argument merely saves the temporary zip file from
# which 'temoa.py' is created.

set -e

TMP_DIR=$(mktemp -d --suffix='.TemoaArchive')

cleanup() {
	# Called unless --debug passed as first argument to script

	\rm -rf "$TMP_DIR"
}

if [[ "$1" != "--debug" ]]; then
	trap cleanup KILL TERM EXIT
fi

PKG_NAME=temoa.py
PKG_PATH=./temoa_model
CWD=$(pwd)

git diff --quiet || (echo "Uncommitted changes in branch.  Exiting ..." && exit 1)
git diff --cached --quiet || (echo "Uncommitted changes in index.  Exiting ..." && exit 1)

VERSION=$(git rev-parse HEAD)
TODAY="$(date -u +"%F")"
( cd "$PKG_PATH"
  find . -name "*.py" -print0 | xargs -0 -I FILES cp FILES "$TMP_DIR"
)

( cd "$TMP_DIR"
  find . -name "*.py" -print0 | xargs -0 \
    sed -i "{
     s|\\(TEMOA_GIT_VERSION \\+= \\)'HEAD'|\\1'$VERSION'|;
     s|\\(TEMOA_RELEASE_DATE \\+= \\)'Today'|\\1'$TODAY'|;
    }"

  find . -name "*.py" -print0 | xargs -0 zip "$PKG_NAME".zip -q9@ --symlinks

  echo "#!/usr/bin/env coopr_python" > "$PKG_NAME"
  cat "$PKG_NAME".zip >> "$PKG_NAME"
  chmod 755 "$PKG_NAME"
  mv "$PKG_NAME" "$CWD"
)

