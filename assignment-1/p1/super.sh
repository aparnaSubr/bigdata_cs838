tez_or_mr=(tez mr)

query_ids=( 12 21 50 71 85 )
#query_ids=( 12 )

num_tries=$1

if [ "$#" -ne 1 ]; then
	echo "You haven't entered num_tries paramter. So, default=1 number of times each query will be run"
	num_tries=1
fi

rm ~/DONE_CAN_SHUTDOWN_NOW.txt


for query_id in "${query_ids[@]}"
do
	for i in `seq 1 $num_tries`
	do  
		for type in "${tez_or_mr[@]}"
		do
			echo ""
			echo "\n \n Query : ${query_id} Try : ${i} Type : ${type}\n"
			echo ""
			# Below line is for q1
			# sh master.sh $type $query_id $i

			# Below line is for parsing q1
			python processTry.py ${query_id} ${i} ${type}
		done
	done
done

#echo "done. you can shut down vms now." >> ~/DONE_CAN_SHUTDOWN_NOW.txt
