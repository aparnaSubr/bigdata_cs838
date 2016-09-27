echo ""
echo "Removing and Repopulating the known hosts file"

rm -f ~/.ssh/known_hosts
ssh -o StrictHostKeyChecking=no vm4 << HERE1
HERE1
ssh -o StrictHostKeyChecking=no vm3 << HERE2
HERE2
ssh -o StrictHostKeyChecking=no vm2 << HERE3
HERE3
ssh -o StrictHostKeyChecking=no vm1 << HERE4
HERE4
