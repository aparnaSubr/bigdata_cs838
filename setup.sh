cd
sudo apt-get update --fix-missing
sudo apt-get -y install openjdk-7-jdk
sudo apt-get -y install pdsh
sudo chown ubuntu:ubuntu /mnt
sudo chown ubuntu:ubuntu /workspace
cd /home/ubuntu
mkdir conf
mkdir software
mkdir workload
mkdir /mnt/logs
mkdir /mnt/logs/apps
mkdir /mnt/logs/hadoop
mkdir /workspace
