Azure :
Changed password to meet 12 character requirement
Made static IP

/workspace :
Data disk - sdc1 for vm1, 2.
Data disk - sdb1 for vm3, 4.

Changed after redeploy.
sdb1 - 30GB, OS, /.
sdc1 - 215GB, temp, /mnt.
sda1 - 50GB, /workspace.


DataNodes fail to start :
Look at logs in /mnt (temp). ClusterId mismatch.
Fix - Delete dn and nn cluster data under hdfs in dn_dirs and nn_dir in /workspace/storage/ ..

ssh failed :
azure vm reset-access <resrcgroup> vm2 -u <uname> -p <newpass>
If there is some error with the VM extension, goto the azure portal -> vm -> extension -> uninstall.

Steps after starting vms:

1. reset access and password
4. reset password-less ssh on all hosts. Use repopulate_known_hosts.sh
	Then can use pdsh -R ssh -w ^instances "ls -l / | grep 'workspace'" etc
2. unmount and mount disks appropriately. Use re_mount_disk.sh <workspace disk> <mnt disk>
3. reset permissions on /mnt and /workspace. SKIP THIS STEP IF USING re_mount_disk.sh!!
5. source run.sh
6. start_all hadoop daemons
7. to start running hive/mr or hive/tez, use scripts in /workload/hive-tpcds-tpch-workload/. Commands formats can be found in gather_query_data.sh

[adbhat : 27/sep/2016 : 6 am]
Scripts: In folder p1
0. on_start_vm1.sh - take a look.
1. master.sh is the main for kicking off the data collection
	a. Calls collector.sh and fetch.sh
	b. dump data in gitPath/results/p1

Hive :
/apps/hive/tpcds__.db
hdfs dfs -h /tmp/tpcds-generate/db_1/50/ - actual data


Varying params :

# --hiveconf mapred.reduce.tasks=val
# --hiveconf mapreduce.reduce.shuffle.parallelcopies=
# --hiveconf mapreduce.job.reduce.slowstart.completedmaps=

MR - Reduce Tasks - verify in output file itself.
MR - Parallel Copies - in history/done/.../conf.xml - grep 'mapreduce.reduce.shuffle.parallelcopies'
MR - Completed Maps - in history/done/.../conf.xml - grep 'mapreduce.job.reduce.slowstart.completedmaps'

# --hiveconf tez.am.container.reuse.enabled=
# --hiveconf tez.runtime.shuffle.parallel.copies=

Tez - Container Reuse - in tez-history - grep 'tez.am.container.reuse.enabled'
Tez - Parallel Copies - in tez-history - grep 'tez.runtime.shuffle.parallel.copies'



