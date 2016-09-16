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