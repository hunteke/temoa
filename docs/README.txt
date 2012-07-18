This directory contains the documentation (in ReST format) for the Temoa
Project.  Provided you have installed sphinx into your coopr checkout, it should
be as simple as running make:

$ make
 -> Error/Help output, showing possible formats

  # to make both the PDF version and a single HTML version of the documentation
$ make latexpdf singlehtml


If you need to install sphinx, you can use Coopr's virtual instance of
easy_install:

$ coopr/bin/easy_install -U sphinx
