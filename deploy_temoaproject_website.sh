#!/bin/bash

set -e  # stop on error

REMOTE_SERVER='temoaproject.org'
UPDDIR='.temoaproject.org-updating'
UPDPKG='.temoaproject.org-updating.tbz'
DELDIR='.temoaproject.org-deleting'
WEBDIR='temoaproject.org'

function usage () {
	BNAME=$(basename "$0")

	cat <<EOF
usage synopsis: $BNAME [--help|--debug]

This script is basically a codification of the steps to deploy to the website.
In other words, since most of the steps can be automated, this scripts does
that, also serving as a written form of the necessary actions to take and
providing some simple sanity checks.

This script also offers a reminder to seed a new torrent file for the
VirtualBox ova file that has become the Temoa Project's preferred method of
supporting Windows.
EOF

	exit 1
}

if [[ "$1" = "--help" ]]; then
	usage
fi

if [[ -e "./docs/" ]]; then
	cat <<EOF
Please remove the directory './docs/'.  This script will destroy anything in
that directory, so save any work you have in it and remove it.
EOF

	exit 1
fi

if [[ -z "$(which pv)" ]]; then
	cat <<EOF
Unable to find the 'pv' (Pipe Viewer) program.  Please install it before
rerunning this script.
EOF

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

Be sure to also install these packages from pip:

    sphinxcontrib-spelling
    sphinxcontrib-bibtex
    pyenchant

Also, if running Ubuntu, you may need to update the 'six' library:

    $ sudo pip install --upgrade six
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
	git checkout --quiet temoaproject.org
	git checkout -- download/index.html  # undo MAGNET_URL
}

if [[ "$1" != "--debug" ]]; then
	trap cleanup KILL TERM EXIT
else
	set -x
fi


echo -e "\nTesting ssh connection to $REMOTE_SERVER"
ssh -n $REMOTE_SERVER
ssh_error="$?"
if [[ "0" != "$ssh_error" ]]; then
	cat <<EOF
Unable to connect to '$REMOTE_SERVER' via ssh.  You will need to correct this
problem before continuing.
EOF

	exit $ssh_error
fi

echo -e "\nMaking temoa.py"

git checkout --quiet energysystem
./create_archive.sh
mv ./temoa.py "$TMP_DIR/"

echo "  Creating example_data_sets.zip"

cp -ra ./data_files/ "$TMP_DIR/example_data_sets/"
( cd "$TMP_DIR/"
  zip -qr9 example_data_sets.zip example_data_sets/
  rm -rf ./example_data_sets/
)

echo -e "\nMaking documentation"

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

echo -e "\nPiecing together website downloads ..."
git checkout --quiet temoaproject.org

mkdir -p ./docs/
mv /tmp/TemoaDocumentationBuild/singlehtml/* ./docs/
mv /tmp/TemoaDocumentationBuild/latex/TemoaProject.pdf ./download/TemoaDocumentation.pdf
mv "$TMP_DIR/"{temoa.py,example_data_sets.zip} ./download/

# Convert '&' to '&amp;' for proper HTML, and escape '&' so that the next sed
# invocation doesn't mistake it for the regex '&'
MAGNET_URL=$(transmission-show -m TemoaBox.ova.torrent | \
             sed "{s/\&/\\\&amp;/g}")

echo "  Writing Magnet URL: $MAGNET_URL"
sed -i "{
	s|REGEX_REPLACE_WITH_MAGNET_URL|$MAGNET_URL|;
}" ./download/index.html

chmod 755 ./download/temoa.py
chmod 644 ./download/{example_data_sets.zip,TemoaDocumentation.pdf}

echo -e "\nUploading to website"
BYTES=$(tar --totals -cf - * .htaccess 2>&1 1> /dev/null | awk {'print $4'})

# We use this convoluted 'tar' pipeline to update the website, rather than a
# a more appropriate method (e.g., rsync), so that we can approach atomicity.
# That is, since our group may update the Temoa website from our respective
# homes, let's try to ensure that the update happens ... or it doesn't.  What we
# don't want, is half an update, and then our internet connection dies (for
# whatever reason).
tar -cf - * .htaccess | pv -s "$BYTES" | bzip2 --best | ssh "$REMOTE_SERVER" "cat > '$UPDPKG'" && \
  ssh "$REMOTE_SERVER" "rm -rf '$UPDDIR' && mkdir '$UPDDIR' && (cd '$UPDDIR'; tar -xf ../'$UPDPKG') && \
   mv '$WEBDIR' '$DELDIR' && mv '$UPDDIR' '$WEBDIR' && rm -rf '$DELDIR' '$UPDPKG'"

