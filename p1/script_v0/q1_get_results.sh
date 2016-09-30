#!/bin/bash

qNum=12
qType=mr
gitLoc=~/bigdata_cs838/
dt=27
iter=1
qFolder=q"$qNum""$qType"

declare -a query_nums=( 12 21 50 71 85 )


# For each iteration
echo "Analysing.."
for iter in "${query_nums[@]}"
do
    echo "Query: $iter"
    qNum=$iter
    qFolder=q"$qNum""$qType"
    loc=$gitLoc/results/q1/$qFolder/$dt/$iter/
    
    # 1. Query completion time 
    #echo "Query Completion time.." 
    runIter=1        # Iterations = 4
    while [ $runIter -lt 4 ]
    do
        loc=$gitLoc/results/q1/$qFolder/$dt/$runIter/
        #echo $loc
        startTime=`cat $loc/stdout_"$qType"_"$qNum".log | grep -i start | awk '{}{print $2}{}'`
        endTime=`cat $loc/stdout_"$qType"_"$qNum".log | grep "End:" | awk '{}{print $2}{}'`

        queryTime=$(( $endTime - $startTime ))
        echo "Start: "$startTime" End: "$endTime" Total: "$queryTime 

        runIter=$(( $runIter + 1 ))
    done
    
    
    # 2. Network
    echo "Network Bytes read/tx.." 
    runIter=1
    while [ $runIter -lt 4 ]        # < 4
    do
        loc=$gitLoc/results/q1/$qFolder/$dt/$runIter
        
        vm=1
        totalRead=0
        totalWrite=0
        while [ $vm -lt 5 ]         # < 5
        do
            netFile=$loc"/vm"$vm"_network_"$qType"_q"$qNum
            #echo $netFile

            startRxNet=`cat $netFile | grep eth0 | awk '{}{print $2}{}' | head -n 1`
            endRxNet=`cat $netFile | grep eth0 | awk '{}{print $2}{}' | tail -n 1`
            
            startTxNet=`cat $netFile | grep eth0 | awk '{}{print $10}{}' | head -n 1`
            endTxNet=`cat $netFile | grep eth0 | awk '{}{print $10}{}' | tail -n 1`
            
            totalRxBytes=$(( $endRxNet - $startRxNet ))
            totalTxBytes=$(( $endTxNet - $startTxNet ))
            
            totalRxMB=$(( $totalRxBytes / 1024 / 1024 ))
            totalTxMB=$(( $totalTxBytes / 1024 / 1024 ))
            
            totalRead=$(( totalRead + $totalRxMB ))
            totalWrite=$(( totalWrite + $totalTxMB ))
            
            #echo -e "Start Rx: "$startRxNet"\t End Rx: "$endRxNet"\t Total Rx: "$totalRxMB "MB"
            #echo -e "Start Tx: "$startTxNet"\t End Tx: "$endTxNet"\t Total Tx: "$totalTxMB "MB"
            
            vm=$(( $vm + 1 ))

        done
        if [ 0 -eq 10 ]
        then
            echo -e "Across 4VM Read: \t $totalRead MB"
            echo -e "Across 4VM Write: \t $totalWrite MB"
        fi
        runIter=$(( $runIter + 1 ))
    done

    # 3. Disk
    echo "Disk Bytes read.." 
    runIter=1
    while [ $runIter -lt 1 ]        # < 4
    do
        loc=$gitLoc/results/q1/$qFolder/$dt/$runIter
        
        vm=1
        totalRead=0
        totalWrite=0
        while [ $vm -lt 5 ]         # < 5
        do
            # Find the partition where workspace was mounted
            mountFile=$loc"/vm"$vm"_mount_"$qType"_q"$qNum
            mountDevice=`cat $mountFile | grep workspace | awk '{}{print $1}{}' | rev | cut -d'/' -f1 | rev`
            #echo $mountDevice

            diskFile=$loc"/vm"$vm"_disk_"$qType"_q"$qNum
            
            # Use that device for grepping
            startReadDisk=`cat $diskFile | grep $mountDevice | awk '{}{print $6}{}' | head -n 1`
            endReadDisk=`cat $diskFile | grep $mountDevice | awk '{}{print $6}{}' | tail -n 1`
            
            startWriteDisk=`cat $diskFile | grep $mountDevice | awk '{}{print $10}{}' | head -n 1`
            endWriteDisk=`cat $diskFile | grep $mountDevice | awk '{}{print $10}{}' | tail -n 1`
            
            totalSectorRead=$(( $endReadDisk - $startReadDisk ))
            totalSectorWrite=$(( $endWriteDisk - $startWriteDisk ))
            
            totalRxMB=$(( $totalSectorRead * 512 / 1024 ))
            totalTxMB=$(( $totalSectorWrite * 512 / 1024 ))
            
            totalRead=$(( totalRead + $totalRxMB ))
            totalWrite=$(( totalWrite + $totalTxMB ))
            #echo -e "Start Rx: "$startReadDisk"\t End Rx: "$endReadDisk"\t Total Rx: "$totalRxMB "B"
            #echo -e "Start Tx: "$startWriteDisk"\t End Tx: "$endWriteDisk"\t Total Tx: "$totalTxMB "B"
            
            vm=$(( $vm + 1 ))

        done
        echo -e "Across 4VM Read: \t $totalRead KB"
        echo -e "Across 4VM Write: \t $totalWrite KB"

        runIter=$(( $runIter + 1 ))
    done
    echo "------------------------------"
done



