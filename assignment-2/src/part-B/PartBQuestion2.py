import sys
from pyspark.sql.types import StructType, StructField, StringType, TimestampType
from pyspark.sql import SparkSession
from pyspark.sql.functions import window

spark = SparkSession.builder\
    .config('spark.master', 'spark://10.254.0.83:7077')\
    .config('spark.app.name', 'CS-838-Assignment2-PartB-1')\
    .config('spark.driver.memory', '8g')\
    .config('spark.eventLog.enabled', 'true')\
    .config('spark.eventLog.dir', 'file:///home/ubuntu/logs/spark')\
    .config('spark.executor.memory', '12g')\
    .config('spark.executor.cores', '4')\
    .config('spark.task.cpus', '1')\
    .getOrCreate()

def main():
    tweet_schema = StructType([StructField('userA', StringType()),\
                              StructField('userB', StringType()),\
                              StructField('timestamp', TimestampType()),\
                              StructField('interaction', StringType())])

    lines = spark.readStream.option('sep', ',').schema(tweet_schema).csv(sys.argv[1])
    mentioned_users = lines.select('userB').where('interaction = \'MT\'')
    query = mentioned_users.writeStream\
                           .outputMode('append')\
                           .format('parquet')\
                           .option('path', '/user/ubuntu/parquet-output')\
                           .option('numRows', '2147483645')\
                           .option('truncate', 'False')\
                           .option('checkpointLocation', '/user/ubuntu/parquet-output' + '_spark_metadata')\
                           .trigger(processingTime='10 seconds')\
                           .start()

    query.awaitTermination()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: $SPARK_HOME/bin/spark-submit PartBQuestion2.py <hdfs-monitoring-directory>')
        sys.exit(0)
    main()
