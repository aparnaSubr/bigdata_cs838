

for queryid in 21
do
	for iter in 1 2 3 4 5 6 7 8 9 0
	do
	(hive --hiveconf hive.execution.engine=tez --hiveconf hive.tez.container.size=4800 --hiveconf hive.tez.java.opts=-Xmx4400m -f sample-queries-tpcds/query${queryid}.sql --database tpcds_text_db_1_50) 2> output/query${queryid}/query${queryid}_tez${iter}.out

	(hive --hiveconf hive.execution.engine=mr -f sample-queries-tpcds/query${queryid}.sql --database tpcds_text_db_1_50) 2> output/query${queryid}/query21_mr${iter}.out
	done
done
