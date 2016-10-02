#!/bin/sh

# $1 = query_id
# $6 = num_reducer
# $7 = parallel_copy
# $8 = comp_maps

# --hiveconf mapred.reduce.tasks=val
# --hiveconf mapreduce.reduce.shuffle.parallelcopies=
# --hiveconf mapreduce.job.reduce.slowstart.completedmaps=

query_id=$1

echo "Start: " $(date +%s)
(time hive --hiveconf hive.execution.engine=mr --hiveconf mapred.reduce.tasks=$2 --hiveconf mapreduce.reduce.shuffle.parallelcopies=$3 --hiveconf mapreduce.job.reduce.slowstart.completedmaps=$4 -f sample-queries-tpcds/query${query_id}.sql --database tpcds_text_db_1_50) 2> output/tpcds_query${query_id}_mr.out
echo "End: " $(date +%s)

