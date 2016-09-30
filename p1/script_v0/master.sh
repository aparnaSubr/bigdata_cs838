#!/bin/bash
# One script to rule them all! -_-
# RUN AS ./master.sh and not sh master.sh


declare -a query_nums=( 12 21 50 71 85 )
#declare -a query_nums=( 12 )
qt=tez
numIters=4

master_output=~/workload/output/master_output.log
total=${#query_nums[*]} 
echo "Total queries: $total" > $master_output 2>&1
#echo "Total queries: $total" 


for i in "${query_nums[@]}"
do 
	query=$i
	iter=1
	echo "Running Query: $query, Query type: $qt" >> $master_output 2>&1
	#echo "Running Query: $query, Query type: $qt" 
	while [ $iter -lt $numIters ]
	do 
		echo "Iter :$iter" >> $master_output 2>&1

		sh ~/workload/collector.sh $query $qt  >> $master_output 2>&1
		ssh vm2 "sh ~/workload/collector.sh $query $qt" >> $master_output 2>&1
		ssh vm3 "sh ~/workload/collector.sh $query $qt" >> $master_output 2>&1
		ssh vm4 "sh ~/workload/collector.sh $query $qt" >> $master_output 2>&1
	
		./run_query_hive_"$qt".sh $query > output/stdout_"$qt"_"$query".log
	
		ssh vm2 "sh ~/workload/fetch.sh $query $qt" >> $master_output 2>&1
		ssh vm3 "sh ~/workload/fetch.sh $query $qt" >> $master_output 2>&1
		ssh vm4 "sh ~/workload/fetch.sh $query $qt" >> $master_output 2>&1
		sh ~/workload/fetch.sh $query $qt $iter >> $master_output 2>&1
		iter=$(( $iter + 1 ))
	done

done
