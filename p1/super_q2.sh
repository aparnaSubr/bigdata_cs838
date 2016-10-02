#tez_or_mr=(tez mr)
tez_or_mr=(mr)

query_ids=( 21 12 50 )
#query_ids=( 21 )

reducers=( 5 )
#reducers=( 1 5 10 20 )
#reducers=( 20 )

#parallel_copies=( 5 )
#parallel_copies=( 5 10 15 20 )
parallel_copies=( 15 )

#completed_maps=( 1 )
completed_maps=( 0.05 0.25 0.5 0.75 1 )

container_reuse=("true" "false")
#container_reuse=("false")

num_tries=$1

if [ "$#" -ne 1 ]; then
	echo "You haven't entered num_tries paramter. So, default=1 number of times each query will be run"
	num_tries=1
fi

workload_dir="/home/ubuntu/workload/hive-tpcds-tpch-workload"
rm -f ${workload_dir}/q2_run_query_hive_mr.sh
rm -f ${workload_dir}/q2_run_query_hive_tez.sh

cp ~/bigdata_cs838/p1/q2_run_query_hive_mr.sh ${workload_dir}/
cp ~/bigdata_cs838/p1/q2_run_query_hive_tez.sh ${workload_dir}/

for i in `seq 1 $num_tries`
do  
	for query_id in "${query_ids[@]}"
	do
		for type in "${tez_or_mr[@]}"
		do
			for pc in "${parallel_copies[@]}"
			do
				if [ $type = "tez" ]; then
					for cr in "${container_reuse[@]}"
					do
						echo ""
						echo ""
						echo "Q${query_id} : Try : ${i} Type : ${type} Container Resuse : ${cr} PllCps : ${pc}"
						echo ""
						echo ""						

						sh master_q2_tez.sh $type $query_id $i $cr $pc

					done

				elif [ $type = "mr" ]; then
					for nr in "${reducers[@]}"
					do
						for cm in "${completed_maps[@]}"
						do
							echo ""
							echo ""
							echo "Q${query_id} : Try : ${i} Type : ${type} Reds : ${nr} PllCps : ${pc} Compl. Maps : ${cm}"
							echo ""
							echo ""

							sh master_q2_mr.sh $type $query_id $i $nr $pc $cm

						done
					done
				fi
			done			
		done
	done
done


