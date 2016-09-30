#!/bin/bash

#kill -9 `ps -ef | grep collector.sh | grep -v grep | awk '{}{print $2}{}'`

# This is called from ~/workload/master.sh
# sh fetch.sh <12,21,50,71,85> <mr/tez> <iter>

host=`hostname`
echo $host
vm_name=`hostname`
query=q"$1"
query_type=$2
run_iter=$3

git_results_folder = "~/bigdata_cs838/results/q1/"

# Network
echo "End" >> ~/workload/output/"$vm_name"_network_"$query_type"_"$query"
cat /proc/net/dev >> ~/workload/output/"$vm_name"_network_"$query_type"_"$query"
echo "------------------" >> ~/workload/output/"$vm_name"_network_"$query_type"_"$query"

# Disk
echo "End" >>  ~/workload/output/"$vm_name"_disk_"$query_type"_"$query"
cat /proc/diskstats >> ~/workload/output/"$vm_name"_disk_"$query_type"_"$query"
echo "------------------" >> ~/workload/output/"$vm_name"_disk_"$query_type"_"$query"


if [ "$host" = "vm1" ]; then 
	if [ "$query_type" = "mr" ]; then 
		echo "MR: Fetching data.."
		scp vm2:~/workload/output/vm2* ~/workload/output/
		scp vm3:~/workload/output/vm3* ~/workload/output/
		scp vm4:~/workload/output/vm4* ~/workload/output/

		echo "Sleeping 60 secs in fetch step.."
		sleep 60

		# Copying from HDFS folder
		dt=`date | awk '{}{print $3}{}'`
		mkdir ~/workload/output/jhist/
		echo $dt
		hdfs dfs -copyToLocal /tmp/hadoop-yarn/staging/history/"done"/2016/09/$dt/000000/* /home/ubuntu/workload/output/jhist/
		hdfs dfs -ls /tmp/hadoop-yarn/staging/history/"done"/2016/09/$dt/000000/
		
		# Cleaning the HDFS folder
		hdfs dfs -rmr /tmp/hadoop-yarn/staging/history/"done"/2016/09/$dt/000000/*
		echo "Contents after deletion"
		echo ""
		echo ""
		echo ""
		hdfs dfs -ls /tmp/hadoop-yarn/staging/history/"done"/2016/09/$dt/000000/

		# Move results to git folder
		cd "$git_results_folder""$query""$query_type"
		mkdir -p $dt/$run_iter/
		cp -r ~/workload/output/* $dt/$run_iter/
		cd ~/workload/output/
		rm -rf *
		cd ..
	fi
	
	if [ "$query_type" = "tez" ]; then 
		echo "Tez: Fetching data.."
		out="/home/ubuntu/workload/output/"
		# Fetch output folder
		scp vm2:~/workload/output/vm2* $out
		scp vm3:~/workload/output/vm3* $out
		scp vm4:~/workload/output/vm4* $out

		# Container files
		appFolder=$out"dot_vm"
		
		# Fetch the results
		echo "Fetching apps folder.."	
		mv /mnt/logs/apps/* $appFolder"1"
		scp -r vm2:/mnt/logs/apps/* $appFolder"2"
		scp -r vm3:/mnt/logs/apps/* $appFolder"3"
		scp -r vm4:/mnt/logs/apps/* $appFolder"4"
		
		# Clean
		echo "Cleaning apps folder.."	
		ssh vm2 "rm -rf /mnt/logs/apps/*"
		ssh vm3 "rm -rf /mnt/logs/apps/*"
		ssh vm4 "rm -rf /mnt/logs/apps/*"

		# Copy from the HDFS folder
		hdfsLocal=$out"hdfs"
		tezHDFS="/tmp/tez-history"
		mkdir -p $hdfsLocal

		hdfs dfs -copyToLocal $tezHDFS $hdfsLocal
		hdfs dfs -ls $tezHDFS
		
		# Cleaning the HDFS folder
		hdfs dfs -rm -r $tezHDFS
		echo "Contents after deletion"
		echo ""
		echo ""
		echo ""
		hdfs dfs -ls $tezHDFS

		# Move results to git folder
		dt=`date | awk '{}{print $3}{}'`
		gitLoc="$git_results_folder""$query""$query_type"
		cd $gitLoc
		mkdir -p $dt/$run_iter/
		echo "Copying everything"
		cp -r /home/ubuntu/workload/output/* $dt/$run_iter/
		rm -rf /home/ubuntu/workload/output/*
		cd $gitLoc/$dt/$run_iter/
		cp `find . -name *.dot` .	
	fi
fi

exit


exit

# git push

git add -A
git commit -m "Pushing"
git push origin master


