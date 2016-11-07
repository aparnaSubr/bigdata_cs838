Execution:
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Part-A

Question 1: ~/software/spark-2.0.0-bin-hadoop2.6/bin/spark-submit ~/part-A/PartAQuestion1.py <hdfs path to input file> <number of iterations>
~/software/spark-2.0.0-bin-hadoop2.6/bin/spark-submit ~/part-A/PartAQuestion1.py </user/ubuntu/web-BerkStan.txt> <10>

Question 2: ~/software/spark-2.0.0-bin-hadoop2.6/bin/spark-submit ~/part-A/PartAQuestion2.py <hdfs path to input file> <number of iterations>
~/software/spark-2.0.0-bin-hadoop2.6/bin/spark-submit ~/part-A/PartAQuestion2.py </user/ubuntu/web-BerkStan.txt> <10>

Question 3: ~/software/spark-2.0.0-bin-hadoop2.6/bin/spark-submit ~/part-A/PartAQuestion3.py <hdfs path to input file> <number of iterations>
~/software/spark-2.0.0-bin-hadoop2.6/bin/spark-submit ~/part-A/PartAQuestion3.py </user/ubuntu/web-BerkStan.txt> <10>

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Part-B

Note:
Scripts for Questions 1, 2 and 3 assume that streaming-emulator.sh will be run separately.
Part-B Questions 1, 2 and 3 reset (delete and re-create) hdfs directory structure before spark-submit.
Part-B Question 3 requires a file named user-ids.csv at hdfs:///user/ubuntu/user-ids.csv

streaming-emulator: ./streaming-emulator.sh

Question 1:  ~/software/spark-2.0.0-bin-hadoop2.6/bin/spark-submit ~/part-B/PartBQuestion1.py <hdfs path to hdfs monitoring directory>
~/software/spark-2.0.0-bin-hadoop2.6/bin/spark-submit ~/part-B/PartBQuestion1.py 'hdfs:///user/ubuntu/monitoring'

Question 2:   ~/software/spark-2.0.0-bin-hadoop2.6/bin/spark-submit ~/part-B/PartBQuestion2.py <hdfs path to hdfs monitoring directory>
~/software/spark-2.0.0-bin-hadoop2.6/bin/spark-submit ~/part-B/PartBQuestion2.py 'hdfs:///user/ubuntu/monitoring'

Question 3:    ~/software/spark-2.0.0-bin-hadoop2.6/bin/spark-submit ~/part-B/PartBQuestion3.py <hdfs path to hdfs monitoring directory>
~/software/spark-2.0.0-bin-hadoop2.6/bin/spark-submit ~/part-B/PartBQuestion3.py 'hdfs:///user/ubuntu/monitoring'

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Part-C
