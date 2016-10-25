
# $1 = tez/mr
# $2 = query_num
# $3 = try_number

if [ "$#" -ne 3 ]; then
        echo "Usage: $0 tez query_num try_num"
        exit
else
        try_number=$3
fi

out_dir="/home/ubuntu/bigdata_cs838/results/$2/$1/try_$try_number/"

echo "\n***** master.sh $1 $2 $3 start\n"

rm -rf $out_dir/*

scp script.sh vm2:~/scripts
scp script.sh vm3:~/scripts
scp script.sh vm4:~/scripts

#before
sh script.sh $1 $2 master before $try_number

ssh vm2 sh ~/scripts/script.sh $1 $2 slave2 before $try_number 
ssh vm3 sh ~/scripts/script.sh $1 $2 slave3 before $try_number 
ssh vm4 sh ~/scripts/script.sh $1 $2 slave4 before $try_number 

#query
echo "\nmaster.sh : Executing query for: $1 query_id=$2 try_num=$3"
sh script.sh $1 $2 master query $try_number

#after
sh script.sh $1 $2 master after $try_number

ssh vm2 sh ~/scripts/script.sh $1 $2 slave2 after $try_number 
ssh vm3 sh ~/scripts/script.sh $1 $2 slave3 after $try_number 
ssh vm4 sh ~/scripts/script.sh $1 $2 slave4 after $try_number 

echo "master.sh : SCPing from slaves : start"

scp -r vm2:$out_dir/slave2 $out_dir 
scp -r vm3:$out_dir/slave3 $out_dir 
scp -r vm4:$out_dir/slave4 $out_dir 

echo "master.sh : SCPing from slaves : end"
echo "\n***** master.sh $1 $2 $3 end\n"
