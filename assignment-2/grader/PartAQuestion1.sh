#!/bin/bash

current_dir=`pwd`

cd
. ~/run.sh
run_hdfs=`jps | grep -i namenode`
if [ ${#run_hdfs} == 0 ]; then
    start_hdfs
else
    echo 'HDFS daemons running.'
fi    

run_spark=`jps | grep -i master`
if [ ${#run_spark} == 0 ]; then
    start_spark
else
    echo 'Spark daemons running.'
fi

cache_clean

~/software/spark-2.0.0-bin-hadoop2.6/bin/spark-submit ~/part-A/PartAQuestion1.py '/user/ubuntu/web-BerkStan.txt' 10

cd $current_dir
