# $1 = tez/mr
# $2 = query_num
# $3 = master/slave
# $4 = before/after/query
# $5 = trial
# $6 = num_reducer
# $7 = parallel_copy
# $8 = comp_maps

model=$1
trial=$5

dev_file_loc="/proc/net/dev"
diskstats_file_loc="/proc/diskstats"

workload_dir="/home/ubuntu/workload/hive-tpcds-tpch-workload"
output_dir="/home/ubuntu/bigdata_cs838/results/q2/$2/$1/nr_$6/pc_$7/cm_$8/try_$trial/$3"

if [ $1 = "tez" ]; then	
		jhist_file_loc="/tmp/tez-history"
else
		jhist_file_loc="/tmp/hadoop-yarn/staging/history"
fi

echo "\n##### script_q2_mr.sh $1 q-$2 $3 $4 t-$5 nr-$6 pc-$7 cm-$8 START #####"

###### BEFORE
# collects disk and network data
if [ $4 = "before" ]; then
	echo "newPass123123$" | sudo -S sh -c "sync; echo 3 > /proc/sys/vm/drop_caches"
	echo "Sudo was for Clearing Cache"
	# deleting .dot file (step: d)
	if [ $1 = "tez" ]; then
		echo "script_q2_mr.sh : Tez : deleting files in /mnt/logs/apps/ "
		rm -rf /mnt/logs/apps/*
	fi

	# deleting, recreating folder structure
	rm -rf $output_dir
	mkdir -p $output_dir

	if [ $3 = "master" ]; then
		echo "script_q2_mr.sh : Deleting " $workload_dir/output
		rm -rf $workload_dir/output/*
		echo "script_q2_mr.sh : Deleting " $jhist_file_loc
		hadoop fs -rm -r $jhist_file_loc
	fi
	
	cp $dev_file_loc $output_dir
	cp $diskstats_file_loc $output_dir
	mv $output_dir/dev $output_dir/dev_before_$1
	mv $output_dir/diskstats $output_dir/diskstats_before_$1

elif [ $4 = "query" ]; then
	if [ $3 = "master" ]; then
		###### QUERY
		cd $workload_dir
		sh $workload_dir/q2_run_query_hive_$1.sh $2 $6 $7 $8 > $output_dir/cmdoutput_$2.txt
		cp $workload_dir/output/tpcds_query$2_$1.out $output_dir
		cd "/home/ubuntu/bigdata_cs838/p1"
	fi
	
else 
	###### AFTER
#	echo "newPass123123$" | sudo -S sh -c "sync; echo 3 > /proc/sys/vm/drop_caches"

	cp $dev_file_loc $output_dir
	cp $diskstats_file_loc $output_dir
	mv $output_dir/dev $output_dir/dev_after_$1
	mv $output_dir/diskstats $output_dir/diskstats_after_$1

	if [ $3 = "master" ]; then		
		echo "script_q2_mr.sh : Going to sleep for 60"
		sleep 60
		echo "script_q2_mr.sh : master : Listing files in HDFS location " $jhist_file_loc
		hadoop fs -ls $jhist_file_loc
		hadoop fs -copyToLocal $jhist_file_loc $output_dir
		echo "##### Listing contents of output dir after copying from HDFS"
		ls -al $output_dir
	fi
	
	if [ $1 = "tez" ]; then
		echo "script_q2_mr.sh : Tez : so copying /mnt/logs/apps/ to output_dir"
		cp -rf /mnt/logs/apps/ $output_dir
	fi
	
	chmod -R 777 $output_dir

	echo "script_q2_mr.sh : output_dir is ====>" $output_dir
	echo "\n##### script_q2_mr.sh $1 q-$2 $3 $4 t-$5 nr-$6 pc-$7 cm-$8 DONE #####"
fi


