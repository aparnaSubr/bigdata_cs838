echo "Creating directories"
cd
#sudo apt-get update --fix-missing
#sudo apt-get -y install openjdk-7-jdk
#sudo apt-get -y install pdsh
sudo chown ubuntu:ubuntu /mnt
sudo chown ubuntu:ubuntu /workspace
cd /home/ubuntu
mkdir conf
mkdir software
mkdir workload
mkdir /mnt/logs
mkdir /mnt/logs/apps
mkdir /mnt/logs/hadoop
#mkdir /workspace
mkdir /workspace/storage
mkdir /workspace/storage/data
mkdir /workspace/storage/data/local
mkdir /workspace/storage/data/local/nm
mkdir /workspace/storage/data/local/tmp
mkdir /workspace/storage/hdfs
mkdir /workspace/storage/hdfs/hdfs_dn_dirs
mkdir /workspace/storage/hdfs/hdfs_nn_dir
echo "Done"
