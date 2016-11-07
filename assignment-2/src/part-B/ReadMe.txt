Part-B

-----------------------------------------------------------------------------------------------------------------------------------------------------

reset-directories.sh:
1. Remove staging and monitoring directories
2. Remove old output files and spark-metadata (if any)
3. Re-create staging and monitoring directories and copy the split-dataset to staging/

-----------------------------------------------------------------------------------------------------------------------------------------------------

hdfs-5s-copy.sh:
Atomically moves one file from the staging directory to the monitoring directory hdfs:///user/ubuntu/staging, hdfs:///user/ubuntu/monitoring

-----------------------------------------------------------------------------------------------------------------------------------------------------

Question 1:
1. tweet_schema specifies the expected input-csv file schema. (userA, userB, timestamp, interaction)
2. lines is a streaming DataFrame constructed by reading the input stream (streaming emulated by moving files into the monitoring directory).
3. windowed_counts is the DataFrame returned after applying the window function (take windows of 1 hour-intervals 
   spaced 30 minutes apart), and counting the number of interactions per group of window-interaction event.
4. ordered_counts reorders windowed_counts in ascending order of window start-times.
5. query is the handler returned to control execution after calling start() on the streaming query.
6. Output mode is 'complete' as aggregation based on window intervals and interaction is done.
   Output is displayed on console.

-----------------------------------------------------------------------------------------------------------------------------------------------------

Question 2:
1. tweet_schema specifies the expected input-csv file schema. (userA, userB, timestamp, interaction)
2. lines is a streaming DataFrame constructed by reading the input stream (streaming emulated by moving files into the monitoring directory).
3. mentioned_users is the DataFrame returned after the SQL query on lines.
   (select userB from lines where interaction = 'MT')
4. query is the handler returned to control execution after calling start() on the streaming query.
5. Output mode is 'append' since no aggregation is performed during the query execution. 
   Output is written as parquet files to HDFS : hdfs:///user/ubuntu/parquet-output.
   Spark checkpoint location on HDFS : hdfs:///user/ubuntu/parquet-output_spark_metadata.
   Trigger interval of 10 seconds processes query every 10 seconds. 
   If execution does not complete before the start of the next trigger interval, processing will begin again at the next trigger interval (and not as soon as execution is complete). 

-----------------------------------------------------------------------------------------------------------------------------------------------------

Question 3:
1. user_id_schema specifies the expected input-csv file schema. (userID)
2. user_ids is a static DataFrame constructed by reading the user-ids.csv file. (hdfs:///user/ubuntu/user-ids.csv)
3. tweet_schema specifies the expected input-csv file schema. (userA, userB, timestamp, interaction)
4. lines is a streaming DataFrame constructed by reading the input stream (streaming emulated by moving files into the monitoring directory).
5. user_interactions is a streaming DataFrame constructed by an inner join of the lines streaming DataFrame with the static user_ids DataFrame, and applying groupBy and count operations to it.
6. query is the handler to control execution after calling start() on the streaming query.
7. Output mode is 'complete' as aggregation based on user-id, interaction groups is done.
   Output is displayed on console.
   Trigger interval of 5 seconds triggers processing every 5 seconds. Processing begins on the next trigger interval if execution does not complete.

-----------------------------------------------------------------------------------------------------------------------------------------------------
