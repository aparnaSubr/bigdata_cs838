
# $1 = tez/mr
# $2 = query_num
# $3 = try_number
# $4 = num_reducer
# $5 = parallel_copy
# $6 = comp_maps

if [ "$#" -ne 6 ]; then
        echo "Usage: $0 tez query_num try_num num_reducer parallel_copy comp_maps"
        exit
else
        try_number=$3
fi

out_dir="/home/ubuntu/bigdata_cs838/results/q2/${query_id}/$1/$4/$5/$6/try_$try_number/"

echo "\n***** master_q2_mr.sh $1 q-$2 t-$3 nr-$4 pc-$5 cm-$6 start\n"

rm -rf $out_dir/*

scp script_q2_mr.sh vm2:~/scripts
scp script_q2_mr.sh vm3:~/scripts
scp script_q2_mr.sh vm4:~/scripts

#before
sh script_q2_mr.sh $1 $2 master before $try_number $4 $5 $6
ssh vm2 sh ~/scripts/script_q2_mr.sh $1 $2 slave2 before $try_number $4 $5 $6
ssh vm3 sh ~/scripts/script_q2_mr.sh $1 $2 slave3 before $try_number $4 $5 $6
ssh vm4 sh ~/scripts/script_q2_mr.sh $1 $2 slave4 before $try_number $4 $5 $6 

#query
echo "\nmaster.sh : Executing query for: $1 query_id=$2 try_num=$3"
sh script_q2_mr.sh $1 $2 master query $try_number $4 $5 $6

#after
sh script_q2_mr.sh $1 $2 master after $try_number $4 $5 $6
ssh vm2 sh ~/scripts/script_q2_mr.sh $1 $2 slave2 after $try_number $4 $5 $6
ssh vm3 sh ~/scripts/script_q2_mr.sh $1 $2 slave3 after $try_number $4 $5 $6 
ssh vm4 sh ~/scripts/script_q2_mr.sh $1 $2 slave4 after $try_number $4 $5 $6 

echo "master.sh : SCPing from slaves : start"

scp -r vm2:$out_dir/slave2 $out_dir 
scp -r vm3:$out_dir/slave3 $out_dir 
scp -r vm4:$out_dir/slave4 $out_dir 

echo "master.sh : SCPing from slaves : end"
echo "\n***** master_q2_mr.sh $1 q-$2 t-$3 nr-$4 pc-$5 cm-$6 end\n"
