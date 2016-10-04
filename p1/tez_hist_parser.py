from __future__ import print_function
import json
import sys
from sys import stdout
import subprocess
import os

"""
These are the main jobs that we are interested in
"""
mr_keys = ["TASK_STARTED", "TASK_FINISHED", "JOB_FINISHED"]
value_keys = ["FILE_BYTES_READ", "FILE_BYTES_WRITTEN", "HDFS_BYTES_READ", "HDFS_BYTES_WRITTEN"]

"""
These are used to create the output directories
"""


def create_output_directories(path):
    if not os.path.exists(path):
        os.makedirs(path)


"""
Process the counts in the groups present so as to extract the useful data
"""


def process_counters(counts, filePtr=None):
    if filePtr == None:
        filePtr = stdout
    for val in counts:
        if val["name"] in value_keys:
            output = val["name"] + ": " + str(val["value"])
            print(output, file=filePtr)


"""
Parse the json object for the event finished type
"""


def parse_finished_job_json(key_value, file_name):
    output_path = "output/FINAL/"
    create_output_directories(output_path)
    with open(output_path + file_name, "w+") as f:
        finished_job = key_value["event"]["org.apache.hadoop.mapreduce.jobhistory.JobFinished"]
        total_tasks = finished_job["finishedMaps"] + finished_job["finishedReduces"] + finished_job["failedMaps"] + finished_job["failedReduces"]
        print("TOTAL_TASKS: " + str(total_tasks), file=f)
        print("FINISHED_MAPS: " + str(finished_job["finishedMaps"]), file=f)
        print("FINISEHD_REDUCES: " + str(finished_job["finishedReduces"]), file=f)
        print("FAILED_MAPS: " + str(finished_job["failedMaps"]), file=f)
        print("FAILED_REDUCES: " + str(finished_job["failedReduces"]), file=f)
        print("MAP_STATUS: ", file=f)
        map_counters = finished_job["mapCounters"]["groups"][0]["counts"]
        process_counters(map_counters, f)
        print("REDUCE_STATUS: ", file=f)
        reduce_counters = finished_job["reduceCounters"]["groups"][0]["counts"]
        process_counters(reduce_counters, f)
        print("TOTAL_STATUS: ", file=f)
        total_counters = finished_job["totalCounters"]["groups"][0]["counts"]
        process_counters(total_counters, f)


"""
Returns a list of all jhist files in the current directory
"""


def get_all_jhist_files(output_file=None):
    file_expr = ".jhist"
    p = subprocess.Popen(['ls'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    jhist_files = [files for files in out.split("\n") if file_expr in files]
    return jhist_files


"""
Prints the key desired in a separate directory of its own
"""


def print_desired_keys(key_value, file_name):
    # print("The dict is ")
    # print(key_value)
    for (k, v) in key_value.items():
        if k == "JOB_FINISHED":
            parse_finished_job_json(v[0], file_name)
        output_path = "output/" + k + "/"
        create_output_directories(output_path)
        with open(output_path + file_name, "w+") as f:
            for vals in v:
                # print(json.dumps(vals, indent=2, sort_keys=True))
                print(json.dumps(vals, indent=2, sort_keys=True), file=f)


"""
Parse individual jshist files

You can pretty print it or use it to populate a dictionary based on
the key desired
"""


def parse_file(file_name):
    with open(file_name) as f:
        file_lines = f.read().split("\n")
        key_value = {}
        output_path = "./output/"
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        outfilepath = output_path + file_name
        with open(outfilepath, "w+") as out_f:
            for lines in file_lines:
                try:
                    jsn = json.loads(lines)
                    # print("The type is : ", jsn["type"])
                    # print("the keys are: ", jsn.keys())
                    if jsn["type"] in mr_keys:
                        if jsn["type"] not in key_value:
                            key_value[jsn["type"]] = list()
                        key_value[jsn["type"]].append(jsn)
                    print(json.dumps(jsn, indent=2, sort_keys=True), file=out_f)
                except:
                    pass
        # print_desired_keys(key_value, file_name)


# for files in jhist_files:
# parse_file(jhist_files)
if __name__ == "__main__":
    parse_file(sys.argv[1])
# jhist_files = get_all_jhist_files()

