This directory contains the documentation (in ReST format) for the Temoa
Project.

1. Installation

Several software elements are required in order to produce this ReST documentation,
which can be installed with a combination of conda and pip:

$ vconda install sphinx
$ pip install sphinx-rtd-theme
$ pip install sphinxcontrib-bibtex
In order to install the spelling module, you need to first install pyenchant, which in
turn requires HomeBrew:
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
Then install pyenchant:
$ brew install enchant
Then spelling module:
$ pip install sphinxcontrib-spelling
Also need to install LaTex itself. On a Mac, that would be MacTeX, which must be manually
downloaded and installed: https://www.tug.org/mactex/mactex-download.html

2. Produce documentation

From the /docs folder, execute the following to generate the html documentation:
$ make html

To generate the PDF documentation, from the same folder, execute the following:

$ make latexpdf

Sometimes this automatic PDF generation fails. If that is the case, navigate to /tmp/TemoaDocumentationBuild/
and manually generate the pdf:

$ pdflatex toolsforenergymodeloptimizationandanalysistemoa.pdf

There seems to be an issue near line 81 with \begin{document}.




