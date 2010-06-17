#!/bin/bash
make clean; make html
echo "Copied new documentation to ./html sub-directory"
cp -r _build/html html 

echo "Copying new documentation to the temoaproject.org website"
scp -r html energym@energy-modeling.org:temoaproject.org/docs 
echo "Documentation updated on the website."
echo "Please visit temoaproject.org/docs to check."
