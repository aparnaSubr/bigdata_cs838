import sys
from pyspark.sql.types import StructType, StructField, StringType, TimestampType
from pyspark.sql import SparkSession

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
    # Static DataFrame
    user_id_schema = StructType([StructField('userID', StringType())])
    user_ids = spark.read.schema(user_id_schema).csv('hdfs:///user/ubuntu/user-ids.csv')

    # Streaming DataFrame
    tweet_schema = StructType([StructField('userA', StringType()),\
                               StructField('userB', StringType()),\
                               StructField('timestamp', TimestampType()),\
                               StructField('interaction', StringType())])

    lines = spark.readStream.option('sep', ',')\
                            .schema(tweet_schema)\
                            .csv(sys.argv[1])


    # Inner join of static DataFrame with Streaming DataFrame to extract relevant rows
    # Compute number of interactions for given users
    user_interactions = lines.join(user_ids, lines.userA == user_ids.userID, 'inner')\
                             .groupBy(lines.userA, lines.interaction)\
                             .count()\
                             .orderBy(lines.userA)

    # Start the query and print to console
    query = user_interactions.writeStream\
                             .outputMode('complete').format('console')\
                             .option('numRows', '2147483645')\
                             .option('truncate', 'False')\
                             .trigger(processingTime='5 seconds')\
                             .start()
    query.awaitTermination()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: PartBQuestion3.py <hdfs-monitoring-directory>')
        sys.exit(0)
    main()
