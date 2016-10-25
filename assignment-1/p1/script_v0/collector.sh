#!/bin/bash

# This is called from ~/workload/master.sh
# sh collector.sh <12,21,50,71,85> <mr/tez>

vm_name=`hostname`
query_id=q"$1"
query_type=$2
host=`hostname`

echo "Starting collector.."
rm -rf ~/workload/output/*

if [ "$host" = "vm1" ]; then
	if [ "$query_type" = "mr" ]; then 
		dt=`date | awk '{}{print $3}{}'`
		hdfs dfs -rm -r /tmp/hadoop-yarn/staging/history/"done"/2016/09/$dt/000000/*
		echo "After cleaning the HDFS directory"
		echo ""
		echo ""
		echo ""
		hdfs dfs -ls /tmp/hadoop-yarn/staging/history/"done"/2016/09/$dt/000000/
	fi

	if [ "$query_type" = "tez" ]; then 
		echo "Running Tez query"			
	
		echo "Creating apps folder.."	
		appFolder="/home/ubuntu/workload/output/dot_vm"
		mkdir -p "$appFolder"1
        mkdir -p "$appFolder"2
        mkdir -p "$appFolder"3
        mkdir -p "$appFolder"4

		echo "After creation.."
		ls ~/workload/output/
		hdfs dfs -rm -r /tmp/tez-history/
		echo "After cleaning the HDFS tez directory"
		echo ""
		echo ""
		echo ""
		hdfs dfs -ls /tmp/tez-history

	fi
fi

# Sudo command doesn't really work
#sudo sh -c "sync; echo 3 > /proc/sys/vm/drop_caches"

# Mount point
df -h > ~/workload/output/"$vm_name"_mount_"$query_type"_"$query_id"

# Network
echo "Start" >> ~/workload/output/"$vm_name"_network_"$query_type"_"$query_id"
cat /proc/net/dev >> ~/workload/output/"$vm_name"_network_"$query_type"_"$query_id"
echo "------------------" >> ~/workload/output/"$vm_name"_network_"$query_type"_"$query_id"

# Disk
echo "Start" >> ~/workload/output/"$vm_name"_disk_"$query_type"_"$query_id"
cat /proc/diskstats >> ~/workload/output/"$vm_name"_disk_"$query_type"_"$query_id"
echo "------------------" >> ~/workload/output/"$vm_name"_disk_"$query_type"_"$query_id" 
