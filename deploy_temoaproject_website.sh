#!/bin/bash

UPDDIR='.temoaproject.org-updating'
UPDPKG='.temoaproject.org-updating.tgz'
DELDIR='.temoaproject.org-deleting'
WEBDIR='temoaproject.org'

tar -cf - * .htaccess | gzip --best | ssh temoaproject.org "cat > .temoaproject.org-updating.tgz" && \
  ssh temoaproject.org "rm -rf '$UPDDIR' && mkdir '$UPDDIR' && (cd '$UPDDIR'; tar -xf ../'$UPDPKG') && \
  mv '$WEBDIR' '$DELDIR' && mv '$UPDDIR' '$WEBDIR' && rm -rf '$DELDIR' '$UPDPKG'"
