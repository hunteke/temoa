#!/bin/bash

set -e  # stop on error

if [[ -e "./docs/" ]]; then
	echo
	echo "Please remove the directory './docs/'.  This script will destroy anything"
	echo "in that directory, so save any work you have in it and remove it."
	echo

	exit 1
fi

if [[ -z "$(which pv)" ]]; then
	echo
	echo "Unable to find the 'pv' (Pipe Viewer) program.  Please install it before"
	echo "rerunning this script."
	echo

	exit 1
fi

if [[ -n "$(git diff)" ]]; then
	echo
	echo "There are unstaged changes.  Appropriately deal with them before running"
	echo "this script."
	echo

	exit 1
fi

UPDDIR='.temoaproject.org-updating'
UPDPKG='.temoaproject.org-updating.tbz'
DELDIR='.temoaproject.org-deleting'
WEBDIR='temoaproject.org'

echo "Making documentation"

git checkout energysystem
( cd docs/
  make spelling
  echo -e "\n\nPotentially misspelled words:\n----------\n"
  cat /tmp/TemoaDocumentationBuild/spelling/output.txt
  echo
  read -p "Type 'continue' if there are no spelling issues: "  NO_SPELLING_ERRORS
  [[ "$NO_SPELLING_ERRORS" != "continue" ]] && exit 1
  make singlehtml
  make latexpdf
)

echo "Making temoa.py"
./create_archive.sh
mv ./temoa.py /tmp/

echo "Creating example_data_sets.zip"
cp -ra ./data_files/ /tmp/example_data_sets/
( cd /tmp
  zip -r -9 example_data_sets.zip example_data_sets/
  rm -rf ./example_data_sets/
)

find . -name "*.pyc" -delete

git checkout temoaproject.org

mkdir -p ./docs/
mv /tmp/TemoaDocumentationBuild/singlehtml/* ./docs/
mv /tmp/TemoaDocumentationBuild/latex/TemoaProject.pdf ./download/
mv /tmp/temoa.py ./download/

chmod 755 ./download/temoa.py
chmod 644 ./download/TemoaProject.pdf

rm -rf /tmp/TemoaDocumentationBuild/

echo "Uploading to website"
BYTES=$(tar --totals -cf - * .htaccess 2>&1 1> /dev/null | awk {'print $4'})

tar -cf - * .htaccess | pv -s "$BYTES" | bzip2 --best | ssh temoaproject.org "cat > '$UPDPKG'" && \
  ssh temoaproject.org "rm -rf '$UPDDIR' && mkdir '$UPDDIR' && (cd '$UPDDIR'; tar -xf ../'$UPDPKG') && \
   mv '$WEBDIR' '$DELDIR' && mv '$UPDDIR' '$WEBDIR' && rm -rf '$DELDIR' '$UPDPKG'"

rm -rf ./docs/
