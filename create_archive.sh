#!/bin/bash

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
