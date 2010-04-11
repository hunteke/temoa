#!/usr/bin/perl

use strict;
use warnings;

# This is crap code.  It is not documented because it's only in the
# repository as a temporary measure, and I do *not* want to encourage
# anyone to rely on this code for anything even remotely mission critical.

while ( <> ) {
	if (    s|^\s+(x[cu])\[([^\]]+)\]\:\s+\n|$1,$2,|
	     || s|^\s+Value: || ) {
		print;
	}
}
