
# Check mounted file system"
echo ""
echo "Did you check the mount points on each VM?"
echo ""
echo ""
 
sh repopulate_known_hosts.sh

echo ""
echo "Changing ownership of folders to ubuntu"
echo ""

ssh vm1 "sudo chown ubuntu:ubuntu /mnt; sudo chown ubuntu:ubuntu /workspace"
ssh vm2 "sudo chown ubuntu:ubuntu /mnt; sudo chown ubuntu:ubuntu /workspace"
ssh vm3 "sudo chown ubuntu:ubuntu /mnt; sudo chown ubuntu:ubuntu /workspace"
ssh vm4 "sudo chown ubuntu:ubuntu /mnt; sudo chown ubuntu:ubuntu /workspace"


host=`hostname`

if [ "$host" = "vm1" ]; then
        echo "Running Start_all.."
	start_all
fi



