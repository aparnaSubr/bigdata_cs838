sudo umount /workspace/
sudo umount /mnt/
sudo mount $1 /workspace/
sudo mount $2 /mnt/
sudo chown ubuntu:ubuntu /mnt/
sudo chown ubuntu:ubuntu /workspace/
