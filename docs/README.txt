This directory contains the documentation (in ReST format) for the Temoa
Project.  Provided you have installed sphinx into your coopr checkout, it should
be as simple as running make:

$ make
 -> Error/Help output, showing possible formats

  # to make both the PDF version and a single HTML version of the documentation
$ make latexpdf singlehtml

In order to generate the formatted source code that is linked to the algebraic equations, run the following:

$ make html

This generates the ‘_modules’ folder, which needs to be placed on the website.

Notes
* Cover page info appears in conf.py
* TemoaDocumentation.pdf goes in temoaproject.org/download folder
* After running ‘make singlehtml’, place resultant ‘index.html’ file in ‘temoaproject.org/docs' folder
* After running ‘make html’, place ‘_modules’ folder in ‘temoaproject.org/docs' folder



If you need to install sphinx, you can use Coopr's virtual instance of
easy_install:

$ coopr/bin/easy_install -U sphinx
