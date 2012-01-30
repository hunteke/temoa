#!/bin/bash

# As of Jan 2012, the generate_scenario_tree.py script no includes the ability
# to create scenarios only for specified stochastic points.  This supposedly
# obsoletes the need for this script.  However, this vim script will remain in
# misc_scripts for the time being, "just in case".

# Usage: ./prune.sh filename
# e.g. ./prune.sh ScenarioStructure.dat

if [ -z $1 ];then
	echo "Usage: ./prune.sh filename"
	exit
fi

# vim -s script.vim $1

STAGE[1]=0
STAGE[2]=0
STAGE[3]=0

# number of stages
NUM_STAGES=3

# final scenario number or max forks in decision tree
MAX_SCENARIO=5

TMP_VIM_SCRIPT=tmpscript.vim

exec 6>&1           # Link file descriptor #6 with stdout.
# Saves stdout.
# Redirect rest of the echo commands in this file to temporary Vim script
exec > ${TMP_VIM_SCRIPT};

# -------------------------- Beginning of output redirection to ${TMP_VIM_SCRIPT} ----------------------------------------------
for i in `seq 1 ${NUM_STAGES} `
do
	for j in `seq 0 ${MAX_SCENARIO} `
	do
		if [[ $j != ${STAGE[$i]} ]]; then
			echo -n ":g/R"

			let tmp="$i-1"
			for k in `seq 1 $tmp `
			do
				echo -n "s${STAGE[$k]}";
			done

			echo -n "s$j"
			echo "/d"
		fi
	done
done

for i in `seq 1 ${NUM_STAGES} `
do
	for j in `seq 0 ${MAX_SCENARIO} `
	do
		if [[ $j != ${STAGE[$i]} ]]; then
			echo -n ":g/Scenario"

			let tmp="$i-1"
			for k in `seq 1 $tmp `
			do
				echo -n "${STAGE[$k]}s";
			done

			echo -n "$j"
			echo "/d"
		fi
	done
done



# Remove lines that contain ';' only that are preceded by blank line
# These are leftovers from removing Children sets
echo ':g/^\n\t;/norm 2dd'
echo ':wq'

# -------------------------- End of output to ${TMP_VIM_SCRIPT} ----------------------------------------------

exec 1>&6 6>&-  # Restore stdout and close file descriptor #6.


# Run vim using the generated script to get the desired pruned tree.
vim -s ${TMP_VIM_SCRIPT} $1

exec 6>&1           # Link file descriptor #6 with stdout.
# Saves stdout.
# Redirect rest of the echo commands in this file to temporary Vim script
exec > filedel-pattern.txt

# -------------------------- Beginning of output redirection to filedel-pattern.txt ----------------------------------------------
for i in `seq 1 ${NUM_STAGES} `
do
	for j in `seq 0 ${MAX_SCENARIO} `
	do
		if [[ $j != ${STAGE[$i]} ]]; then
			echo -n "R"

			let tmp="$i-1"
			for k in `seq 1 $tmp `
			do
				echo -n "s${STAGE[$k]}";
			done

			echo "s$j"
		fi
	done
done

# -------------------------- End of output to filedel-pattern.txt ----------------------------------------------

exec 1>&6 6>&-  # Restore stdout and close file descriptor #6.

for i in `cat filedel-pattern.txt`
do
	 echo $i;
	 echo $i* | xargs rm ;
done
