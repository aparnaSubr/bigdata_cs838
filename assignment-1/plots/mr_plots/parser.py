import os
import sys
import glob
import json
import fnmatch
from pprint import pprint



path = sys.argv[1]
task_all_data = {}
task_map_data = {}
task_reduce_data = {}
totalMaps =0
totalReduces = 0

#for filename in glob.glob(os.path.join(path, '*.jhist')):

matches = []
for root, dirnames, filenames in os.walk(path):
    for filename in fnmatch.filter(filenames, '*.jhist'):
        matches.append(os.path.join(root, filename))
	
#for filename in glob.glob(os.path.join(path, '*.jhist')):
for filename in matches:
	print "Now using {}".format(filename)  
	with open(filename) as data_file:  
		i =0  
		for line in data_file:
			if i==0 or i==2 or line == "\n":
				i+=1
				continue
			data = json.loads(line)
			i+=1
			if (data["type"] == "JOB_INITED"):
				totalMaps += data["event"]["org.apache.hadoop.mapreduce.jobhistory.JobInited"]["totalMaps"]
				totalReduces += data["event"]["org.apache.hadoop.mapreduce.jobhistory.JobInited"]["totalReduces"]
	
			if (data["type"] == "TASK_STARTED"):
				task_all_data[data["event"]["org.apache.hadoop.mapreduce.jobhistory.TaskStarted"]["taskid"]] = [data["event"]["org.apache.hadoop.mapreduce.jobhistory.TaskStarted"]["taskType"],(data["event"]["org.apache.hadoop.mapreduce.jobhistory.TaskStarted"]["startTime"]/1000)]
				if (data["event"]["org.apache.hadoop.mapreduce.jobhistory.TaskStarted"]["taskType"] == "MAP"):
					task_map_data[data["event"]["org.apache.hadoop.mapreduce.jobhistory.TaskStarted"]["taskid"]] = [(data["event"]["org.apache.hadoop.mapreduce.jobhistory.TaskStarted"]["startTime"]/1000)]
				if (data["event"]["org.apache.hadoop.mapreduce.jobhistory.TaskStarted"]["taskType"] == "REDUCE"):
					task_reduce_data[data["event"]["org.apache.hadoop.mapreduce.jobhistory.TaskStarted"]["taskid"]] = [(data["event"]["org.apache.hadoop.mapreduce.jobhistory.TaskStarted"]["startTime"]/1000)]

			
			if (data["type"] == "TASK_FINISHED"):
				task_all_data[data["event"]["org.apache.hadoop.mapreduce.jobhistory.TaskFinished"]["taskid"]].append((data["event"]["org.apache.hadoop.mapreduce.jobhistory.TaskFinished"]["finishTime"]/1000))			
				if (data["event"]["org.apache.hadoop.mapreduce.jobhistory.TaskFinished"]["taskType"] == "MAP"):
					task_map_data[data["event"]["org.apache.hadoop.mapreduce.jobhistory.TaskFinished"]["taskid"]].append((data["event"]["org.apache.hadoop.mapreduce.jobhistory.TaskFinished"]["finishTime"]/1000))
				if (data["event"]["org.apache.hadoop.mapreduce.jobhistory.TaskFinished"]["taskType"] == "REDUCE"):
					task_reduce_data[data["event"]["org.apache.hadoop.mapreduce.jobhistory.TaskFinished"]["taskid"]].append((data["event"]["org.apache.hadoop.mapreduce.jobhistory.TaskFinished"]["finishTime"]/1000))


print "Task all data"
print "-----------------------------"
for i in task_all_data:
	print i, task_all_data[i]
print "\n"
print "Task MAP data"
print "-----------------------------"
for i in task_map_data:
	print i, task_map_data[i]
print "\n"
print "Task Reduce data"
print "-----------------------------"
for i in task_reduce_data:
	print i, task_reduce_data[i]
print "\n"

	
#print task_all_data[min(task_all_data, key=task_all_data.get)]

min_all_data = 20000000000000	
max_all_data = 0	
for i in task_all_data:
	if task_all_data[i][1] < min_all_data:
		min_all_data = task_all_data[i][1]	
	if task_all_data[i][2] > max_all_data:
		max_all_data = task_all_data[i][2]	
print "Min All data: ",min_all_data
print "Max All data: ",max_all_data


min_map_data = 20000000000000	
max_map_data = 0	
for i in task_map_data:
	if task_map_data[i][0] < min_map_data:
		min_map_data = task_map_data[i][0]	
	if task_map_data[i][1] > max_map_data:
		max_map_data = task_map_data[i][1]	
print "Min Map data: ",min_map_data
print "Max Map data: ",max_map_data


min_reduce_data = 20000000000000	
max_reduce_data = 0	
for i in task_reduce_data:
	if task_reduce_data[i][0] < min_reduce_data:
		min_reduce_data = task_reduce_data[i][0]	
	if task_reduce_data[i][1] > max_reduce_data:
		max_reduce_data = task_reduce_data[i][1]	
print "Min Reduce data: ",min_reduce_data
print "Max Reduce data: ",max_reduce_data


diff_all = ((max_all_data) - (min_all_data)) + 1
diff_min = ((max_map_data) - (min_map_data)) + 1
diff_max = ((max_reduce_data) - (min_reduce_data)) + 1


task_all_list = [int(0)]*((max_all_data) - (min_all_data) + 2)
task_map_list = [int(0)]*((max_all_data) - (min_all_data) + 2)
task_reduce_list = [int(0)]*((max_all_data) - (min_all_data) + 2)

# All data
for i in range(min_all_data,max_all_data +1):
	for j in task_all_data:
		if i >= task_all_data[j][1] and i <= task_all_data[j][2]:
			task_all_list[i-min_all_data] += 1
print "All data" 
for task_iter in task_all_list:
    print task_iter

# Map data
for i in range(min_all_data,max_all_data +1):
	for j in task_map_data:
		if i >= task_map_data[j][0] and i <= task_map_data[j][1]:
			task_map_list[i-min_all_data] += 1
print "Map data"
for map_iter in task_map_list:
    print map_iter

# Reduce data
for i in range(min_all_data,max_all_data +1):
	for j in task_reduce_data:
		if i >= task_reduce_data[j][0] and i <= task_reduce_data[j][1]:
			task_reduce_list[i-min_all_data] += 1
print "Reduce data"
for reduce_iter in task_reduce_list:
    print reduce_iter


print "Total Maps: ",totalMaps
print "Total Reduces: ",totalReduces
