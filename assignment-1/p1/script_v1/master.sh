
# $1 = tez/mr
# $2 = query_num
# $3 = try_number

if [ "$#" -ne 3 ]; then
        echo "Usage: $0 tez query_num try_num"
        exit
else
        try_number=$3
fi

out_dir="/home/ubuntu/query_run_output/$2/$1/try_$try_number/"

rm -rf $out_dir/*

scp script.sh vm1:~/scripts
scp script.sh vm3:~/scripts
scp script.sh vm4:~/scripts

#before
sh script.sh $1 $2 master before $try_number

ssh vm1 sh ~/scripts/script.sh $1 $2 slave1 before $try_number 
ssh vm3 sh ~/scripts/script.sh $1 $2 slave3 before $try_number 
ssh vm4 sh ~/scripts/script.sh $1 $2 slave4 before $try_number 

#query
echo "Executing query for: $1 query_id=$2 try_num=$3"
sh script.sh $1 $2 master query $try_number

#after
sh script.sh $1 $2 master after $try_number

ssh vm1 sh ~/scripts/script.sh $1 $2 slave1 after $try_number 
ssh vm3 sh ~/scripts/script.sh $1 $2 slave3 after $try_number 
ssh vm4 sh ~/scripts/script.sh $1 $2 slave4 after $try_number 

scp -r vm1:$out_dir/slave1 $out_dir 
scp -r vm3:$out_dir/slave3 $out_dir 
scp -r vm4:$out_dir/slave4 $out_dir 
