# $1 = tez/mr
# $2 = query_num
# $3 = master/slave
# $4 = before/after/query
# $5 = try_number



try_number=$5
workload_dir="/home/ubuntu/workload/hive-tpcds-tpch-workload"
model=$1
output_dir="/home/ubuntu/query_run_output/$2/$1/try_$try_number/$3"
dev_file_loc="/proc/net/dev"
diskstats_file_loc="/proc/diskstats"

if [ $1 = "tez" ]; then	
		jhist_file_loc="/tmp/tez-history"
else
		jhist_file_loc="/tmp/hadoop-yarn/staging/history"
fi
	

###### BEFORE
if [ $4 = "before" ]; then
	echo "Group14838" | sudo -S sh -c "sync; echo 3 > /proc/sys/vm/drop_caches"
	# deleting .dot file (step: d)
	if [ $1 = "tez" ]; then
		echo "deleting files in /mnt/logs/apps/ "
		rm -rf /mnt/logs/apps/*
	fi

	# deleting if the output dir already exists
	rm -rf $output_dir
	mkdir -p $output_dir

	if [ $3 = "master" ]; then
		rm -rf output/*
		hadoop fs -rm -r $jhist_file_loc
	fi
	
	cp $dev_file_loc $output_dir
	mv $output_dir/dev $output_dir/dev_before_$1
	cp $diskstats_file_loc $output_dir
	mv $output_dir/diskstats $output_dir/diskstats_before_$1

elif [ $4 = "query" ]; then
	
	if [ $3 = "master" ]; then
		###### QUERY
		cd $workload_dir
		sh run_query_hive_$1.sh $2 > $output_dir/cmdoutput_$2.txt
		cp output/tpcds_query$2_$1.out $output_dir
	fi
	
else 
	###### AFTER
	 echo "Group10838" | sudo -S sh -c "sync; echo 3 > /proc/sys/vm/drop_caches"


	cp $dev_file_loc $output_dir
	mv $output_dir/dev $output_dir/dev_after_$1
	cp $diskstats_file_loc $output_dir
	mv $output_dir/diskstats $output_dir/diskstats_after_$1

	if [ $3 = "master" ]; then
		hadoop fs -copyToLocal $jhist_file_loc $output_dir
		echo "###################################"
		ls -al $output_dir
	fi
	
	if [ $1 = "tez" ]; then
		echo "it is tez so copying /mnt/logs/apps/ to output_dir"
		cp -rf /mnt/logs/apps/ $output_dir
	fi
	
	chmod -R 777 $output_dir

	echo "output_dir is ====> "
	echo $output_dir
fi
