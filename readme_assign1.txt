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
2. unmount and mount disks appropriately. Use re_mount_disk.sh <workspace disk> <mnt disk>
3. reset permissions on /mnt and /workspace. SKIP THIS STEP IF USING re_mount_disk.sh!!
4. reset password-less ssh on all hosts. Use repopulate_known_hosts.sh
5. source run.sh
6. start_all hadoop daemons
7. to start running hive/mr or hive/tez, use scripts in /workload/hive-tpcds-tpch-workload/. Commands formats can be found in gather_query_data.sh
