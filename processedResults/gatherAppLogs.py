import sys, os, shutil

mr_or_tez = 'mr'

query_ids = ['12', '21', '50', '71', '85']

trial = '1'

base_dir = "/u/a/d/adbhat/private/gitRepository/bigdata_cs838/results"
outDir = "/u/a/d/adbhat/private/gitRepository/bigdata_cs838/processedResults/q1/"+mr_or_tez+"_logs"

outDir1 = os.path.join(outDir, "history")
outDir2 = os.path.join(outDir, "out")
if os.path.exists(outDir1):
    shutil.rmtree(outDir1)

os.makedirs(outDir1)
if os.path.exists(outDir2):
    shutil.rmtree(outDir2)

os.makedirs(outDir2)

for query_id in query_ids:
    queryDir = os.path.join(base_dir, query_id, mr_or_tez, "try_" + trial, "master")

    # log files - tez
    if mr_or_tez == 'tez':
        inDir1 = os.path.join(queryDir, "tez-history")
        outPath1 = os.path.join(outDir1,"q" + query_id + "_" + mr_or_tez + "_try_" + trial +"_history.txt")

        for f in os.listdir(inDir1):
            shutil.copy(os.path.join(inDir1, f), outPath1)

    # log files - mr
    if mr_or_tez == "mr":

        inDir1 = os.path.join(queryDir, "history/done/2016/10/01/000000")
        outPath1 = os.path.join(outDir1, "q" + query_id + "_" + mr_or_tez + "_try_" + trial);
        if os.path.exists(outPath1):
            shutil.rmtree(outPath1)
        shutil.copytree(inDir1, outPath1)

    # .out Files
    shutil.copy(os.path.join(queryDir, "tpcds_query"+query_id+"_"+mr_or_tez+".out"), os.path.join(outDir2, "q" + query_id + "_" + mr_or_tez + "_try" + trial +"_out.txt"))
