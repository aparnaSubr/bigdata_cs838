ssh-keygen -f "/u/a/d/adbhat/.ssh/known_hosts" -R cs838fall2016group141.eastus.cloudapp.azure.com
ssh-keygen -f "/u/a/d/adbhat/.ssh/known_hosts" -R cs838fall2016group142.eastus.cloudapp.azure.com
ssh-keygen -f "/u/a/d/adbhat/.ssh/known_hosts" -R cs838fall2016group143.eastus.cloudapp.azure.com
ssh-keygen -f "/u/a/d/adbhat/.ssh/known_hosts" -R cs838fall2016group144.eastus.cloudapp.azure.com
gnome-terminal -e "bash -c \"ssh ubuntu@cs838fall2016group141.eastus.cloudapp.azure.com; exec bash\"" &
gnome-terminal -e "bash -c \"ssh ubuntu@cs838fall2016group142.eastus.cloudapp.azure.com; exec bash\"" &
gnome-terminal -e "bash -c \"ssh ubuntu@cs838fall2016group143.eastus.cloudapp.azure.com; exec bash\"" &
gnome-terminal -e "bash -c \"ssh ubuntu@cs838fall2016group144.eastus.cloudapp.azure.com; exec bash\"" &
