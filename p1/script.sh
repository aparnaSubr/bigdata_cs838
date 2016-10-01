# $1 = tez/mr
# $2 = query_num
# $3 = master/slave
# $4 = before/after/query
# $5 = trial

model=$1
trial=$5

dev_file_loc="/proc/net/dev"
diskstats_file_loc="/proc/diskstats"

workload_dir="/home/ubuntu/workload/hive-tpcds-tpch-workload"
output_dir="/home/ubuntu/bigdata_cs838/results/$2/$1/try_$trial/$3"

if [ $1 = "tez" ]; then	
		jhist_file_loc="/tmp/tez-history"
else
		jhist_file_loc="/tmp/hadoop-yarn/staging/history"
fi
	

echo "##### script.sh $1 $2 $3 $4 $5 START #####\n"

###### BEFORE
# collects disk and network data
if [ $4 = "before" ]; then
	echo "newPass123123$" | sudo -S sh -c "sync; echo 3 > /proc/sys/vm/drop_caches"
	echo "Sudo was for Clearing Cache"
	# deleting .dot file (step: d)
	if [ $1 = "tez" ]; then
		echo "Tez : deleting files in /mnt/logs/apps/ "
		rm -rf /mnt/logs/apps/*
	fi

	# deleting if the output dir already exists
	rm -rf $output_dir
	mkdir -p $output_dir

	if [ $3 = "master" ]; then
		rm -rf $workload_dir/output/*
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
		sh $workload_dir/run_query_hive_$1.sh $2 > $output_dir/cmdoutput_$2.txt
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
		hadoop fs -copyToLocal $jhist_file_loc $output_dir
		echo "##### Listing contents of output dir after copying from HDFS"
		ls -al $output_dir
	fi
	
	if [ $1 = "tez" ]; then
		echo "Tez : so copying /mnt/logs/apps/ to output_dir"
		cp -rf /mnt/logs/apps/ $output_dir
	fi
	
	chmod -R 777 $output_dir

	echo "output_dir is ====>" $output_dir
	echo "##### script.sh $1 $2 $3 $4 $5 DONE #####\n"
fi


