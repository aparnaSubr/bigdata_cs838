
# $1 = tez/mr
# $2 = query_num
# $3 = try_number
# $4 = container_reuse
# $5 = parallel_copy


if [ "$#" -ne 5 ]; then
        echo "Usage: $0 tez query_num try_num container_resue parallel_copy"
        exit
else
        try_number=$3
fi

out_dir="/home/ubuntu/bigdata_cs838/results/q2/$2/$1/cr_$4/pc_$5/try_$try_number/"

echo "\n***** master_q2_tez.sh $1 q-$2 t-$3 cr-$4 pc-$5 start\n"

rm -rf $out_dir/*

scp script_q2_tez.sh vm2:~/scripts
scp script_q2_tez.sh vm3:~/scripts
scp script_q2_tez.sh vm4:~/scripts

#before
sh script_q2_tez.sh $1 $2 master before $try_number $4 $5
ssh vm2 sh ~/scripts/script_q2_tez.sh $1 $2 slave2 before $try_number $4 $5
ssh vm3 sh ~/scripts/script_q2_tez.sh $1 $2 slave3 before $try_number $4 $5
ssh vm4 sh ~/scripts/script_q2_tez.sh $1 $2 slave4 before $try_number $4 $5 

#query
echo "\nmaster.sh : Executing query for: $1 query_id=$2 try_num=$3"
sh script_q2_tez.sh $1 $2 master query $try_number $4 $5

#after
sh script_q2_tez.sh $1 $2 master after $try_number $4 $5
ssh vm2 sh ~/scripts/script_q2_tez.sh $1 $2 slave2 after $try_number $4 $5
ssh vm3 sh ~/scripts/script_q2_tez.sh $1 $2 slave3 after $try_number $4 $5 
ssh vm4 sh ~/scripts/script_q2_tez.sh $1 $2 slave4 after $try_number $4 $5 

echo "master.sh : SCPing from slaves : start"

scp -r vm2:$out_dir/slave2 $out_dir 
scp -r vm3:$out_dir/slave3 $out_dir 
scp -r vm4:$out_dir/slave4 $out_dir 

echo "master.sh : SCPing from slaves : end"
echo "\n***** master_q2_tez.sh $1 q-$2 t-$3 cr-$4 pc-$5 end\n"
