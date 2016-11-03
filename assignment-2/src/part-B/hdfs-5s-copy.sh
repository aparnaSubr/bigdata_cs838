#!/bin/bash
for i in `ls ./staging/ | sort -V`;
do
    hadoop fs -mv "/user/ubuntu/staging/"$i "/user/ubuntu/monitoring/"
    sleep 5
done
