echo "Cleaning up directories..."
hdfs dfs -rm -r -skipTrash /user/ubuntu/staging
hdfs dfs -rm -r -skipTrash /user/ubuntu/monitoring
echo "Creating directory structure..."
hdfs dfs -mkdir /user/ubuntu/staging
hdfs dfs -mkdir /user/ubuntu/monitoring
echo "Copying files..."
hadoop fs -cp /user/ubuntu/split-dataset/* /user/ubuntu/staging
echo "Done."
