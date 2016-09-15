Azure :
Changed password to meet 12 character requirement
Made static IP

/workspace :
Data disk - sdc1 for vm1, 2.
Data disk - sdb1 for vm3, 4.

DataNodes fail to start :
Look at logs in /mnt (temp). ClusterId mismatch.
Fix - Delete dn and nn cluster data under hdfs in dn_dirs and nn_dir in /workspace/hadoop/ ..