#!/bin/sh

# --hiveconf tez.am.container.reuse.enabled=
# --hiveconf tez.runtime.shuffle.parallel.copies=

containerJvm="-Xmx4600m"
containerSize=4800

query_id=$1
# container_reuse=$2
# parallel_copy=$3

echo "Start: " $(date +%s)
(time hive --hiveconf hive.execution.engine=tez --hiveconf hive.tez.container.size=$containerSize --hiveconf hive.tez.java.opts=$containerJvm --hiveconf tez.am.container.reuse.enabled=$2 --hiveconf tez.runtime.shuffle.parallel.copies=$3 -f sample-queries-tpcds/query${query_id}.sql --database tpcds_text_db_1_50) 2> output/tpcds_query${query_id}_tez.out
echo "End: " $(date +%s)

