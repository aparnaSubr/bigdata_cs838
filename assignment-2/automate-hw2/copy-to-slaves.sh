#!/bin/bash
PASSED_ARG=$1
PASSED_DIR=$2
for i in 2 3 4 5;
do
	if [ -d $PASSED_ARG ]
		then echo "Copying directory $PASSED_ARG to slave-"$i;
		     scp -r $PASSED_ARG vm-14-$i:$PASSED_DIR
	elif [ -f $PASSED_ARG ]
		then echo "Copying file $PASSED_ARG to slave-"$i;
		     scp $PASSED_ARG vm-14-$i:$PASSED_DIR
		else
	    		echo "$PASSED_ARG is not a valid file or directory.";
	    		exit 1
	fi
done
