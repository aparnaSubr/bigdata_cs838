echo "Cleaning up directories..."
hdfs dfs -rm -r -skipTrash /user/ubuntu/staging
hdfs dfs -rm -r -skipTrash /user/ubuntu/monitoring
hdfs dfs -rm -r -skipTrash /user/ubuntu/parquet-output_spark_metadata
hdfs dfs -rm -r -skipTrash /user/ubuntu/parquet-output
echo "Creating directory structure..."
hdfs dfs -mkdir /user/ubuntu/staging
hdfs dfs -mkdir /user/ubuntu/monitoring
hdfs dfs -mkdir /user/ubuntu/parquet-output
echo "Copying files..."
hadoop fs -cp /user/ubuntu/split-dataset/* /user/ubuntu/staging
echo "Done."
