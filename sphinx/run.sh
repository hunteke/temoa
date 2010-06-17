#!/bin/bash
make clean; make html
echo "Copied new documentation to ./html sub-directory"
cp -r _build/html html 

echo -e "\n\nCopying new documentation to the temoaproject.org website\n\n"
scp -r html energym@energy-modeling.org:temoaproject.org/docs 
echo "Documentation updated on the website."
echo -e "\n\n Please visit http://temoaproject.org/docs to check.\n\n"
