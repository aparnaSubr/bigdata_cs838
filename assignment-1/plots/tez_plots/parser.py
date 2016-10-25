import os
import sys
import glob
import json
from pprint import pprint


runnable_list = ["q12tez","q21tez","q50tez","q71tez","q85tez"]
q12tez = {'6':'Map', '5':'Map', '1':'Reducer', '2':'Reducer', '3': 'Reducer', '4': 'Reducer' }
q21tez = {'4':'Map', '5':'Map', '6':'Map', '1':'Reducer', '2': 'Reducer', '3':'Reducer' }
q50tez = {'1':'Map', '7':'Map', '6':'Map', '8':'Map', '5':'Map', '2':'Reducer', '3':'Reducer', '4':'Reducer' }
q71tez = {'7': 'Map', '10':'Map', '9':'Map', '11':'Map', '5':'Map', '6':'Reducer', '8':'Reducer','1':'Reducer', '3':'Reducer', '4':'Reducer' }
q85tez = {'12': 'Map', '13':'Map', '11':'Map', '8':'Map', '7':'Map', '10':'Map', '1':'Reducer', '9':'Reducer','2':'Reducer', '3':'Reducer', '4':'Reducer', '5':'Reducer', '6':'Reducer'}


for number in runnable_list:

    path = '/u/a/p/aparnasubr/Documents/Fall2016/838/tez_plots' + number   
    print path
    exit

    vertex_data = {}
    task_all_data = {}
    task_map_data = {}
    task_reduce_data = {}
    totalMaps =0
    totalReduces = 0
    
    for filename in glob.glob(os.path.join(path, '*')):
        with open(filename) as data_file:  
            i =0  
            for line in data_file:
                data = json.loads(line[:-2])
                i+=1
                if (data["entitytype"] == "TEZ_VERTEX_ID" and data["events"][0]["eventtype"] == "VERTEX_INITIALIZED"):
                    if number == "q12tez":
                        job_type =  q12tez[data["otherinfo"]["vertexName"].split(" ")[1]]
                    if number == "q21tez":
                        job_type =  q21tez[data["otherinfo"]["vertexName"].split(" ")[1]]
                    if number == "q50tez":
                        job_type =  q50tez[data["otherinfo"]["vertexName"].split(" ")[1]]
                    if number == "q71tez":
                        job_type =  q71tez[data["otherinfo"]["vertexName"].split(" ")[1]]
                    if number == "q85tez":
                        job_type =  q85tez[data["otherinfo"]["vertexName"].split(" ")[1]]
                    #print job_type
                    vertex_data[data["entity"]] = job_type
                if (data["entitytype"] == "TEZ_TASK_ID" and data["events"][0]["eventtype"] == "TASK_STARTED"):
                    task_all_data[data["entity"]] = [vertex_data[data["relatedEntities"][0]["entity"]],data["otherinfo"]["startTime"]/1000]
                    if (vertex_data[data["relatedEntities"][0]["entity"]] == "Map"):
                        totalMaps+=1
                        task_map_data[data["entity"]] = [data["otherinfo"]["startTime"]/1000]
                    if (vertex_data[data["relatedEntities"][0]["entity"]] == "Reducer"):
                        totalReduces+=1
                        task_reduce_data[data["entity"]] = [data["otherinfo"]["startTime"]/1000]
                if (data["entitytype"] == "TEZ_TASK_ID" and data["events"][0]["eventtype"] == "TASK_FINISHED"):
                    task_all_data[data["entity"]].append(data["otherinfo"]["endTime"]/1000)
                    task_all_data[data["entity"]][1] = data["otherinfo"]["startTime"]/1000  # ??, start times dont match, stupid file
                    if(task_all_data[data["entity"]][0] == "Map"):
                        task_map_data[data["entity"]][0] = data["otherinfo"]["startTime"]/1000  # ??, start times dont match, stupid file
                        task_map_data[data["entity"]].append(data["otherinfo"]["endTime"]/1000)
                    if(task_all_data[data["entity"]][0] == "Reducer"):
                        task_reduce_data[data["entity"]][0] = data["otherinfo"]["startTime"]/1000  # ??, start times dont match, stupid file
                        task_reduce_data[data["entity"]].append(data["otherinfo"]["endTime"]/1000)
    
    '''
    print "Vertex data"
    print "-----------------------------"
    for i in vertex_data:
        print i, vertex_data[i]
    print "\n"
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
    
    print totalMaps
    print totalReduces
    '''
    
    fall = open(number+"_all.txt","wb")
    fmap = open(number+"_map.txt","wb")
    fred = open(number+"_red.txt","wb")
    fstats = open(number+"_stats.txt","wb")
        
    print >> fstats, "Total Maps: ",totalMaps
    print >> fstats, "Total Reduces: ",totalReduces
    
    #print task_all_data[min(task_all_data, key=task_all_data.get)]
    
    min_all_data = 20000000000000   
    max_all_data = 0    
    for i in task_all_data:
        if task_all_data[i][1] < min_all_data:
            min_all_data = task_all_data[i][1]  
        if task_all_data[i][2] > max_all_data:
            max_all_data = task_all_data[i][2]  
    #print "Min All data: ",min_all_data
    #print "Max All data: ",max_all_data
    
    
    min_map_data = 20000000000000   
    max_map_data = 0    
    for i in task_map_data:
        if task_map_data[i][0] < min_map_data:
            min_map_data = task_map_data[i][0]  
        if task_map_data[i][1] > max_map_data:
            max_map_data = task_map_data[i][1]  
    #print "Min Map data: ",min_map_data
    #print "Max Map data: ",max_map_data
    
    
    min_reduce_data = 20000000000000    
    max_reduce_data = 0 
    for i in task_reduce_data:
        if task_reduce_data[i][0] < min_reduce_data:
            min_reduce_data = task_reduce_data[i][0]    
        if task_reduce_data[i][1] > max_reduce_data:
            max_reduce_data = task_reduce_data[i][1]    
    #print "Min Reduce data: ",min_reduce_data
    #print "Max Reduce data: ",max_reduce_data
    
    
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
        print >> fall, task_iter
    
    # Map data
    for i in range(min_all_data,max_all_data +1):
        for j in task_map_data:
            if i >= task_map_data[j][0] and i <= task_map_data[j][1]:
                task_map_list[i-min_all_data] += 1
    print "Map data"
    for map_iter in task_map_list:
        print >> fmap, map_iter
    
    # Reduce data
    for i in range(min_all_data,max_all_data +1):
        for j in task_reduce_data:
            if i >= task_reduce_data[j][0] and i <= task_reduce_data[j][1]:
                task_reduce_list[i-min_all_data] += 1
    print "Reduce data"
    for reduce_iter in task_reduce_list:
        print >> fred, reduce_iter
    
#print "Total Maps: "
#print "Total Reduces: ",totalReduces
