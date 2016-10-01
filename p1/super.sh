tez_or_mr=(tez mr)

#query_ids=( 12 21 50 71 85 )
query_ids=( 12 )

num_tries=$1

if [ "$#" -ne 1 ]; then
	echo "You haven't entered num_tries paramter. So, default=1 number of times each query will be run"
	num_tries=1
fi

for query_id in "${query_ids[@]}"
do
	for i in `seq 1 $num_tries`
	do  
		for type in "${tez_or_mr[@]}"
		do
			echo "\n\n Query : ${query_id} Try : ${num_tries} Type : ${type}\n"
			sh master.sh $type $query_id $i
		done
	done
done
