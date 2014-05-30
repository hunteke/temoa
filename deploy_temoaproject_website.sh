#!/bin/bash

set -e  # stop on error

REMOTE_SERVER='temoaproject.org'
UPDDIR='.temoaproject.org-updating'
UPDPKG='.temoaproject.org-updating.tbz'
DELDIR='.temoaproject.org-deleting'
WEBDIR='temoaproject.org'

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

if [[ -z "$(which coopr_python)" ]]; then
	cat <<EOF
Unable to find Coopr (coopr_python).  Please install it, or appropriately modify
your path before continuing.
EOF

	exit 1
fi

if [[ -z "$(which sphinx-build)" ]]; then
	cat <<EOF
Unable to find sphinx-build utility.  Building the documentation requires
Sphinx.  Please install it before continuing.

Note that Sphinx is installable via pip.  If you install to your system
directories, use sudo.  If you wish to install within Coopr, use Coopr's pip:

      # install to system directories
    $ sudo pip install sphinx

      # install within Coopr's directories
    $ $(dirname $(which coopr_python))/pip install sphinx
EOF

	exit 1
fi

git diff --quiet || (echo "Uncommitted changes in branch. Exiting ..." && exit 1)
git diff --cached --quiet || (echo "Uncommitted changes in index. Exiting ..." && exit 1)

if [[ ! -e "TemoaBox.ova.torrent" ]]; then
	cat <<EOF
No torrent file (TemoaBox.ova.torrent).

Since the Temoa Project supports Windows via a VirtualBox appliance, and the
resulting OVA file is generally large, we offer it as a download via the
bittorrent protocol.  Necessary steps to complete prior to executing this
script:

  * create an OVA file through your favorite means (e.g., build a functioning
    system in VirtualBox and export it as an appliance)

  * create a torrent file of the OVA file (e.g., use transmission-create,
    transmission-gtk, Deluge, uTorrent ...)

  * start seeding the torrent somewhere (CRITICAL; NOT YET SCRIPT IMPLEMENTED)

  * place a copy of TemoaBox.ova.torrent in this directory

(And yes, there is no reason for this script to need the .torrent file, other
than as a reminder to you to have created and started it.  :-) )
EOF

	exit 1
else

	echo -e "\nHave you started seeding the new OVA torrent?"
	read -p "Type 'yes' to confirm that you've started the seed: " SEED_STARTED

	[[ "$SEED_STARTED" != "yes" ]] &&
	  echo -e "\n  Please start seeding the torrent." &&
	  exit 1
fi

TMP_DIR=$(mktemp -d --suffix='.DeployTemoaWebsite')

function cleanup () {
	# Called unless --debug passed as first argument to script

	\rm -rf "$TMP_DIR"
	\rm -rf /tmp/TemoaDocumentationBuild/
	\rm -rf ./docs/
	\rm -f ./download/temoa.py
	\rm -f ./download/TemoaDocumentation.pdf
	\rm -f ./download/example_data_sets.zip
}

if [[ "$1" != "--debug" ]]; then
	trap cleanup KILL TERM EXIT
else
	set -x
fi


echo "Testing ssh connection to $REMOTE_SERVER"
ssh -n $REMOTE_SERVER
ssh_error="$?"
if [[ "0" != "$?" ]]; then
	echo
	echo "Unable to connect to '$REMOTE_SERVER' via ssh.  You will need to correct"
	echo "this problem before continuing."
	echo

	exit $ssh_error
fi

echo "Making temoa.py"

git checkout energysystem
./create_archive.sh
mv ./temoa.py "$TMP_DIR/"

echo "Creating example_data_sets.zip"

cp -ra ./data_files/ "$TMP_DIR/example_data_sets/"
( cd "$TMP_DIR/"
  zip -qr9 example_data_sets.zip example_data_sets/
  rm -rf ./example_data_sets/
)

echo "Making documentation"

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

find . -name "*.pyc" -delete

git checkout temoaproject.org

mkdir -p ./docs/
mv /tmp/TemoaDocumentationBuild/singlehtml/* ./docs/
mv /tmp/TemoaDocumentationBuild/latex/TemoaProject.pdf ./download/TemoaDocumentation.pdf
mv "$TMP_DIR/"{temoa.py,example_data_sets.zip} ./download/

chmod 755 ./download/temoa.py
chmod 644 ./download/{example_data_sets.zip,TemoaDocumentation.pdf}

echo "Uploading to website"
BYTES=$(tar --totals -cf - * .htaccess 2>&1 1> /dev/null | awk {'print $4'})

tar -cf - * .htaccess | pv -s "$BYTES" | bzip2 --best | ssh "$REMOTE_SERVER" "cat > '$UPDPKG'" && \
  ssh "$REMOTE_SERVER" "rm -rf '$UPDDIR' && mkdir '$UPDDIR' && (cd '$UPDDIR'; tar -xf ../'$UPDPKG') && \
   mv '$WEBDIR' '$DELDIR' && mv '$UPDDIR' '$WEBDIR' && rm -rf '$DELDIR' '$UPDPKG'"

