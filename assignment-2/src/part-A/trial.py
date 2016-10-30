from __future__ import division
from pyspark import SparkConf, SparkContext
import re
import sys
from operator import add

conf = SparkConf()
conf.set("spark.master", "spark://10.254.0.83:7077")
conf.set("spark.app.name", "CS-838-Assignment2-PartA-1")
conf.set("spark.driver.memory", "1g")
conf.set("spark.eventLog.enabled", "true")
conf.set("spark.eventLog.dir", "file:///home/ubuntu/logs/spark")
conf.set("spark.executor.memory", "1g")
conf.set("spark.executor.cores", "4")
conf.set("spark.task.cpus", "1")
#conf.set("spark.deploy.defaultCores", "")
#conf.set("spark.executor.instances", "20")
#conf.set("spark.default.parallelism", "100")

sc = SparkContext(conf = conf)

def valid_lines(line):
    line = str(line)
    if line.startswith('#'):
        return False
    return True

def split_from_to(line):
    line = str(line)
    split = line.split('\t')
    print(split)
    return (split[0].strip(), split[1].strip())

def calculate_contributions(urls, rank):
    num_links = len(urls)
    for url in urls:
        yield (url, float(rank) / float(num_links) )

def main():
    links = sc.textFile('hdfs://' + sys.argv[1], 75).filter(valid_lines).map(split_from_to).distinct().groupByKey().partitionBy(30)

    num_iterations = int(sys.argv[2])
    ranks = links.mapValues(lambda node : 1.0) 
    
    for i in range(num_iterations):
        contributions = links.join(ranks).flatMap( lambda x : calculate_contributions(x[1][0], x[1][1]) )
        ranks = contributions.reduceByKey(add).mapValues(lambda x : 0.15 + 0.85 * x )

    num = 1
    for (link, rank) in ranks.collect():
        print('{2}. Node {0} : Rank {1}'.format(link, rank, num) )
        num += 1

    sc.stop()
    
if __name__ == '__main__':
    main()
