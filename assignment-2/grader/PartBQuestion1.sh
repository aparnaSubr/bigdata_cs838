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

run_hive=`jps | grep -i runjar`
if [ ${#run_hive} == 0 ]; then
    hive --service metastore &
else
    echo 'Hive metastore running.'
fi

. ~/part-B/reset-directories.sh

~/software/spark-2.0.0-bin-hadoop2.6/bin/spark-submit ~/part-B/PartBQuestion1.py 'hdfs:///user/ubuntu/monitoring'

trap SIGHUP SIGKILL SIGTERM SIGINT

cd $current_dir
