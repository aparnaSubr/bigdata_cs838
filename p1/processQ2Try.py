import sys, os, os.path, getpass, tarfile, glob, shutil, commands, re, errno


def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occured

def printUsage():
    print "Usage: python processTry.py <queryId>"


def errorOutIfPathNotExists(path):
    if (not os.path.exists(path)):
        print "The specified path does not exist : " + path
        sys.exit()


def getMasterData(masterDir, queryId, type):
    outLines = ""
    query_out_filePath = os.path.join(masterDir, "tpcds_query" + queryId + "_" + type + ".out")
    query_out_file = open(query_out_filePath, 'r')
    for inLine in query_out_file:
        if "Time taken:" in inLine and "Fetched:" in inLine:
            outLines += inLine.split(", ")[0].replace(":", ":\t").replace(" seconds", "\tseconds").strip() + "\n"
            outLines += inLine.split(", ")[1].replace(":", ":\t").replace(" row", "\trow").strip() + "\n"
    return outLines


def processProcNetDevData(procNetDevFilePath):
    errorOutIfPathNotExists(procNetDevFilePath)
    procNetDevFile = open(procNetDevFilePath, 'r')

    op_dict = dict()
    for inLine in procNetDevFile:
        if "eth" in inLine or "lo" in inLine:
            fragments = inLine.split()  # multiple spaces by default

            innerDict = {"rx": fragments[1], "tx": fragments[9]}
            op_dict[fragments[0].strip(':')] = innerDict

    # for debug
    # print procNetDevFilePath
    # print op_dict
    return op_dict


# https://www.kernel.org/doc/Documentation/ABI/testing/procfs-diskstats
def processProcDiskstatsData(procDiskstatsFilePath):
    errorOutIfPathNotExists(procDiskstatsFilePath)
    procDiskstatsFile = open(procDiskstatsFilePath, 'r')

    op_dict = dict()
    for inLine in procDiskstatsFile:
        if "sd" in inLine:
            fragments = inLine.split()
            if "1" in fragments[2]:
                innerDict = {"read": fragments[5].strip(), "write": fragments[9].strip()}
                op_dict[fragments[2]] = innerDict

    # debug
    # print "\nDiskstat : " + procDiskstatsFilePath
    # print op_dict
    return op_dict


def getNetStats(dir, type):
    # ['eth0'|'lo']['rx'|tx']
    beforeNetBytes = processProcNetDevData(os.path.join(dir, "dev_before_" + type))
    afterNetBytes = processProcNetDevData(os.path.join(dir, "dev_after_" + type))

    diffNetBytes = dict()
    diffNetBytes['eth0'] = dict()
    diffNetBytes['lo'] = dict()

    diffNetBytes['eth0']['rx'] = int(afterNetBytes['eth0']['rx']) - int(beforeNetBytes['eth0']['rx'])
    diffNetBytes['eth0']['tx'] = int(afterNetBytes['eth0']['tx']) - int(beforeNetBytes['eth0']['tx'])

    diffNetBytes['lo']['rx'] = int(afterNetBytes['lo']['rx']) - int(beforeNetBytes['lo']['rx'])
    diffNetBytes['lo']['tx'] = int(afterNetBytes['lo']['tx']) - int(beforeNetBytes['lo']['tx'])

    # debug
    # print "NetStats\n" + str(diffNetBytes)
    return diffNetBytes


def getDiskStats(dir, type):
    # 0, 1, 2 - sda1, sdb1, sdc1
    # 1, 2 - bytes read, bytes written
    beforeDiskBytes = processProcDiskstatsData(os.path.join(dir, "diskstats_before_" + type))
    afterDiskBytes = processProcDiskstatsData(os.path.join(dir, "diskstats_after_" + type))

    diffDiskBytes = dict()
    diffDiskBytes['sda1'] = dict()
    diffDiskBytes['sdb1'] = dict()
    diffDiskBytes['sdc1'] = dict()

    diffDiskBytes['sda1']['read'] = (int(afterDiskBytes['sda1']['read']) - int(beforeDiskBytes['sda1']['read'])) * 512
    diffDiskBytes['sda1']['write'] = (int(afterDiskBytes['sda1']['write']) - int(beforeDiskBytes['sda1']['write'])) * 512

    diffDiskBytes['sdb1']['read'] = (int(afterDiskBytes['sdb1']['read']) - int(beforeDiskBytes['sdb1']['read'])) * 512
    diffDiskBytes['sdb1']['write'] = (int(afterDiskBytes['sdb1']['write']) - int(beforeDiskBytes['sdb1']['write'])) * 512

    diffDiskBytes['sdc1']['read'] = (int(afterDiskBytes['sdc1']['read']) - int(beforeDiskBytes['sdc1']['read'])) * 512
    diffDiskBytes['sdc1']['write'] = (int(afterDiskBytes['sdc1']['write']) - int(beforeDiskBytes['sdc1']['write'])) * 512

    # debug
    # print "Diff DiskStats\n" + str(diffDiskBytes)
    return diffDiskBytes


def compareVaryingNumReducers(queryTypeDir, outFile, queryId, type="mr", trialNum="1"):
    pc = '5'
    cm = '1'

    nrs = ['1', '5', '10', '20']

    for nr in nrs:
        inDir = os.path.join(queryTypeDir, "nr_" + nr, "pc_" + pc, "cm_" + cm, "try_1")
        try:
            lines = ""
            # lines = inDir + "\n"
            lines += "Query" + queryId + "\t" + type + "\tnr" + nr + "\tpc" + pc + "\tcm" + cm + "\ttrial" + trialNum + "\n"

            slaveDirNames = ["master", "slave2", "slave3", "slave4"]
            lines += getMasterData(os.path.join(inDir, "master"), queryId, type)
            print "Master data:\n" + lines

            netStats = dict()
            diskStats = dict()

            totNetStats = dict()
            totNetStats['lo'] = dict()
            totNetStats['eth0'] = dict()
            totNetStats['lo']['rx'] = 0
            totNetStats['lo']['tx'] = 0
            totNetStats['eth0']['rx'] = 0
            totNetStats['eth0']['tx'] = 0

            totDiskStats = dict()
            totDiskStats['read'] = 0
            totDiskStats['write'] = 0

            for slaveDirName in slaveDirNames:
                netStats[slaveDirName] = getNetStats(os.path.join(inDir, slaveDirName), type)
                diskStats[slaveDirName] = getDiskStats(os.path.join(inDir, slaveDirName), type)

                totNetStats['lo']['rx'] += netStats[slaveDirName]['lo']['rx']
                totNetStats['lo']['tx'] += netStats[slaveDirName]['lo']['tx']

                totNetStats['eth0']['rx'] += netStats[slaveDirName]['eth0']['rx']
                totNetStats['eth0']['tx'] += netStats[slaveDirName]['eth0']['tx']

                totDiskStats['read'] += diskStats[slaveDirName]['sda1']['read']
                totDiskStats['read'] += diskStats[slaveDirName]['sdb1']['read']
                totDiskStats['read'] += diskStats[slaveDirName]['sdc1']['read']

                totDiskStats['write'] += diskStats[slaveDirName]['sda1']['write']
                totDiskStats['write'] += diskStats[slaveDirName]['sdb1']['write']
                totDiskStats['write'] += diskStats[slaveDirName]['sdc1']['write']

            # print "NetStats: "+str(netStats)
            # print "Diskstats: "+str(diskStats)
            print "TotNetStats:\n" + str(totNetStats)
            print "TotDiskstats: " + str(totDiskStats)

            lines += "TotalNetStats\n"
            lines += "eth0 rx (MB)\teth0 tx (MB)\tlo rx (MB)\tlo tx (MB)\n"
            lines += str(totNetStats['eth0']['rx']/(1024*1024)) + "\t" + str(totNetStats['eth0']['tx']/(1024*1024)) + "\t" + str(totNetStats['lo']['rx']/(1024*1024)) + "\t" + str(totNetStats['lo']['tx']/(1024*1024))
            lines += "\n"
            lines += "\nTotalDiskStats\n"
            lines += "Read (MB)\tWrite (MB)\n"
            lines += str(totDiskStats['read']/(1024*1024)) + "\t" + str(totDiskStats['write']/(1024*1024)) + "\n"

            lines += "\n"
            lines += "\n"

            print "\n\nOutput\n" + lines

            with open(outFile, "a") as myfile:
                myfile.write(lines)
        except:
            print "Some error"
            with open(outFile, "a") as myfile:
                myfile.write("Some error")



def compareVaryingParallelCopies(queryTypeDir, outFile, nr, queryId, type="mr", trialNum='1'):

    cm = '1'

    pcs = ['5', '10', '15', '20']

    for pc in pcs:
        inDir = os.path.join(queryTypeDir, "nr_" + nr, "pc_" + pc, "cm_" + cm, "try_1")
        try:
            lines = ""
            # lines = inDir + "\n"
            lines += "Query" + queryId + "\t" + type + "\tnr" + nr + "\tpc" + pc + "\tcm" + cm + "\ttrial" + trialNum + "\n"

            slaveDirNames = ["master", "slave2", "slave3", "slave4"]
            lines += getMasterData(os.path.join(inDir, "master"), queryId, type)
            print "Master data:\n" + lines

            netStats = dict()
            diskStats = dict()

            totNetStats = dict()
            totNetStats['lo'] = dict()
            totNetStats['eth0'] = dict()
            totNetStats['lo']['rx'] = 0
            totNetStats['lo']['tx'] = 0
            totNetStats['eth0']['rx'] = 0
            totNetStats['eth0']['tx'] = 0

            totDiskStats = dict()
            totDiskStats['read'] = 0
            totDiskStats['write'] = 0

            for slaveDirName in slaveDirNames:
                netStats[slaveDirName] = getNetStats(os.path.join(inDir, slaveDirName), type)
                diskStats[slaveDirName] = getDiskStats(os.path.join(inDir, slaveDirName), type)

                totNetStats['lo']['rx'] += netStats[slaveDirName]['lo']['rx']
                totNetStats['lo']['tx'] += netStats[slaveDirName]['lo']['tx']

                totNetStats['eth0']['rx'] += netStats[slaveDirName]['eth0']['rx']
                totNetStats['eth0']['tx'] += netStats[slaveDirName]['eth0']['tx']

                totDiskStats['read'] += diskStats[slaveDirName]['sda1']['read']
                totDiskStats['read'] += diskStats[slaveDirName]['sdb1']['read']
                totDiskStats['read'] += diskStats[slaveDirName]['sdc1']['read']

                totDiskStats['write'] += diskStats[slaveDirName]['sda1']['write']
                totDiskStats['write'] += diskStats[slaveDirName]['sdb1']['write']
                totDiskStats['write'] += diskStats[slaveDirName]['sdc1']['write']

            # print "NetStats: "+str(netStats)
            # print "Diskstats: "+str(diskStats)
            print "TotNetStats:\n" + str(totNetStats)
            print "TotDiskstats: " + str(totDiskStats)

            lines += "TotalNetStats\n"
            lines += "eth0 rx (MB)\teth0 tx (MB)\tlo rx (MB)\tlo tx (MB)\n"
            lines += str(totNetStats['eth0']['rx']/(1024*1024)) + "\t" + str(totNetStats['eth0']['tx']/(1024*1024)) + "\t" + str(totNetStats['lo']['rx']/(1024*1024)) + "\t" + str(totNetStats['lo']['tx']/(1024*1024))
            lines += "\n"
            lines += "\nTotalDiskStats\n"
            lines += "Read (MB)\tWrite (MB)\n"
            lines += str(totDiskStats['read']/(1024*1024)) + "\t" + str(totDiskStats['write']/(1024*1024)) + "\n"

            lines += "\n"
            lines += "\n"

            print "\n\nOutput\n" + lines

            with open(outFile, "a") as myfile:
                myfile.write(lines)
        except:
            print "Some error"
            with open(outFile, "a") as myfile:
                myfile.write("Some error")


def compareVaryingCompletedMaps(queryTypeDir, outFile, nr, pc, queryId, type = "mr", trialNum='1'):

    cms = ['0.05', '0.25', '0.50', '0.75', '1']

    for cm in cms:
        inDir = os.path.join(queryTypeDir, "nr_" + nr, "pc_" + pc, "cm_" + cm, "try_1")
        try:
            lines = ""
            # lines = inDir + "\n"
            lines += "Query" + queryId + "\t" + type + "\tnr" + nr + "\tpc" + pc + "\tcm" + cm + "\ttrial" + trialNum + "\n"

            slaveDirNames = ["master", "slave2", "slave3", "slave4"]
            lines += getMasterData(os.path.join(inDir, "master"), queryId, type)
            print "Master data:\n" + lines

            netStats = dict()
            diskStats = dict()

            totNetStats = dict()
            totNetStats['lo'] = dict()
            totNetStats['eth0'] = dict()
            totNetStats['lo']['rx'] = 0
            totNetStats['lo']['tx'] = 0
            totNetStats['eth0']['rx'] = 0
            totNetStats['eth0']['tx'] = 0

            totDiskStats = dict()
            totDiskStats['read'] = 0
            totDiskStats['write'] = 0

            for slaveDirName in slaveDirNames:
                netStats[slaveDirName] = getNetStats(os.path.join(inDir, slaveDirName), type)
                diskStats[slaveDirName] = getDiskStats(os.path.join(inDir, slaveDirName), type)

                totNetStats['lo']['rx'] += netStats[slaveDirName]['lo']['rx']
                totNetStats['lo']['tx'] += netStats[slaveDirName]['lo']['tx']

                totNetStats['eth0']['rx'] += netStats[slaveDirName]['eth0']['rx']
                totNetStats['eth0']['tx'] += netStats[slaveDirName]['eth0']['tx']

                totDiskStats['read'] += diskStats[slaveDirName]['sda1']['read']
                totDiskStats['read'] += diskStats[slaveDirName]['sdb1']['read']
                totDiskStats['read'] += diskStats[slaveDirName]['sdc1']['read']

                totDiskStats['write'] += diskStats[slaveDirName]['sda1']['write']
                totDiskStats['write'] += diskStats[slaveDirName]['sdb1']['write']
                totDiskStats['write'] += diskStats[slaveDirName]['sdc1']['write']

            # print "NetStats: "+str(netStats)
            # print "Diskstats: "+str(diskStats)
            print "TotNetStats:\n" + str(totNetStats)
            print "TotDiskstats: " + str(totDiskStats)

            lines += "TotalNetStats\n"
            lines += "eth0 rx (MB)\teth0 tx (MB)\tlo rx (MB)\tlo tx (MB)\n"
            lines += str(totNetStats['eth0']['rx']/(1024*1024)) + "\t" + str(totNetStats['eth0']['tx']/(1024*1024)) + "\t" + str(totNetStats['lo']['rx']/(1024*1024)) + "\t" + str(totNetStats['lo']['tx']/(1024*1024))
            lines += "\n"
            lines += "\nTotalDiskStats\n"
            lines += "Read (MB)\tWrite (MB)\n"
            lines += str(totDiskStats['read']/(1024*1024)) + "\t" + str(totDiskStats['write']/(1024*1024)) + "\n"

            lines += "\n"
            lines += "\n"

            print "\n\nOutput\n" + lines

            with open(outFile, "a") as myfile:
                myfile.write(lines)
        except:
            print "Some error"
            with open(outFile, "a") as myfile:
                myfile.write("Some error")


def compareVaryingContainerReuse(queryTypeDir, outFile, queryId, type="tez", trialNum='1'):

    pc = '5'
    crs = ['true', 'false']

    for cr in crs:
        inDir = os.path.join(queryTypeDir, "cr_" + cr, "pc_" + pc, "try_1")
        try:
            lines = ""
            # lines = inDir + "\n"
            lines += "Query" + queryId + "\t" + type + "\tpc" + pc + "\tcr" + cr + "\ttrial" + trialNum + "\n"

            slaveDirNames = ["master", "slave2", "slave3", "slave4"]
            lines += getMasterData(os.path.join(inDir, "master"), queryId, type)
            print "Master data:\n" + lines

            netStats = dict()
            diskStats = dict()

            totNetStats = dict()
            totNetStats['lo'] = dict()
            totNetStats['eth0'] = dict()
            totNetStats['lo']['rx'] = 0
            totNetStats['lo']['tx'] = 0
            totNetStats['eth0']['rx'] = 0
            totNetStats['eth0']['tx'] = 0

            totDiskStats = dict()
            totDiskStats['read'] = 0
            totDiskStats['write'] = 0

            for slaveDirName in slaveDirNames:
                netStats[slaveDirName] = getNetStats(os.path.join(inDir, slaveDirName), type)
                diskStats[slaveDirName] = getDiskStats(os.path.join(inDir, slaveDirName), type)

                totNetStats['lo']['rx'] += netStats[slaveDirName]['lo']['rx']
                totNetStats['lo']['tx'] += netStats[slaveDirName]['lo']['tx']

                totNetStats['eth0']['rx'] += netStats[slaveDirName]['eth0']['rx']
                totNetStats['eth0']['tx'] += netStats[slaveDirName]['eth0']['tx']

                totDiskStats['read'] += diskStats[slaveDirName]['sda1']['read']
                totDiskStats['read'] += diskStats[slaveDirName]['sdb1']['read']
                totDiskStats['read'] += diskStats[slaveDirName]['sdc1']['read']

                totDiskStats['write'] += diskStats[slaveDirName]['sda1']['write']
                totDiskStats['write'] += diskStats[slaveDirName]['sdb1']['write']
                totDiskStats['write'] += diskStats[slaveDirName]['sdc1']['write']

            # print "NetStats: "+str(netStats)
            # print "Diskstats: "+str(diskStats)
            print "TotNetStats:\n" + str(totNetStats)
            print "TotDiskstats: " + str(totDiskStats)

            lines += "TotalNetStats\n"
            lines += "eth0 rx (MB)\teth0 tx (MB)\tlo rx (MB)\tlo tx (MB)\n"
            lines += str(totNetStats['eth0']['rx']/(1024*1024)) + "\t" + str(totNetStats['eth0']['tx']/(1024*1024)) + "\t" + str(totNetStats['lo']['rx']/(1024*1024)) + "\t" + str(totNetStats['lo']['tx']/(1024*1024))
            lines += "\n"
            lines += "\nTotalDiskStats\n"
            lines += "Read (MB)\tWrite (MB)\n"
            lines += str(totDiskStats['read']/(1024*1024)) + "\t" + str(totDiskStats['write']/(1024*1024)) + "\n"

            lines += "\n"
            lines += "\n"

            print "\n\nOutput\n" + lines

            with open(outFile, "a") as myfile:
                myfile.write(lines)
        except:
            print "Some error"
            with open(outFile, "a") as myfile:
                myfile.write("Some error")


def compareVaryingParallelCopies_tez(queryTypeDir, outFile, cr, queryId, type="tez", trialNum='1'):

    pcs = ['5', '10', '15', '20']

    for pc in pcs:
        inDir = os.path.join(queryTypeDir, "cr_" + cr, "pc_" + pc, "try_1")
        try:
            lines = ""
            # lines = inDir + "\n"
            lines += "Query" + queryId + "\t" + type + "\tpc" + pc + "\tcr" + cr + "\ttrial" + trialNum + "\n"

            slaveDirNames = ["master", "slave2", "slave3", "slave4"]
            lines += getMasterData(os.path.join(inDir, "master"), queryId, type)
            print "Master data:\n" + lines

            netStats = dict()
            diskStats = dict()

            totNetStats = dict()
            totNetStats['lo'] = dict()
            totNetStats['eth0'] = dict()
            totNetStats['lo']['rx'] = 0
            totNetStats['lo']['tx'] = 0
            totNetStats['eth0']['rx'] = 0
            totNetStats['eth0']['tx'] = 0

            totDiskStats = dict()
            totDiskStats['read'] = 0
            totDiskStats['write'] = 0

            for slaveDirName in slaveDirNames:
                netStats[slaveDirName] = getNetStats(os.path.join(inDir, slaveDirName), type)
                diskStats[slaveDirName] = getDiskStats(os.path.join(inDir, slaveDirName), type)

                totNetStats['lo']['rx'] += netStats[slaveDirName]['lo']['rx']
                totNetStats['lo']['tx'] += netStats[slaveDirName]['lo']['tx']

                totNetStats['eth0']['rx'] += netStats[slaveDirName]['eth0']['rx']
                totNetStats['eth0']['tx'] += netStats[slaveDirName]['eth0']['tx']

                totDiskStats['read'] += diskStats[slaveDirName]['sda1']['read']
                totDiskStats['read'] += diskStats[slaveDirName]['sdb1']['read']
                totDiskStats['read'] += diskStats[slaveDirName]['sdc1']['read']

                totDiskStats['write'] += diskStats[slaveDirName]['sda1']['write']
                totDiskStats['write'] += diskStats[slaveDirName]['sdb1']['write']
                totDiskStats['write'] += diskStats[slaveDirName]['sdc1']['write']

            # print "NetStats: "+str(netStats)
            # print "Diskstats: "+str(diskStats)
            print "TotNetStats:\n" + str(totNetStats)
            print "TotDiskstats: " + str(totDiskStats)

            lines += "TotalNetStats\n"
            lines += "eth0 rx (MB)\teth0 tx (MB)\tlo rx (MB)\tlo tx (MB)\n"
            lines += str(totNetStats['eth0']['rx']/(1024*1024)) + "\t" + str(totNetStats['eth0']['tx']/(1024*1024)) + "\t" + str(totNetStats['lo']['rx']/(1024*1024)) + "\t" + str(totNetStats['lo']['tx']/(1024*1024))
            lines += "\n"
            lines += "\nTotalDiskStats\n"
            lines += "Read (MB)\tWrite (MB)\n"
            lines += str(totDiskStats['read']/(1024*1024)) + "\t" + str(totDiskStats['write']/(1024*1024)) + "\n"

            lines += "\n"
            lines += "\n"

            print "\n\nOutput\n" + lines

            with open(outFile, "a") as myfile:
                myfile.write(lines)
        except:
            print "Some error"
            with open(outFile, "a") as myfile:
                myfile.write("Some error")



if (len(sys.argv) != 2):
    print("Not enough arguments: " + str(len(sys.argv)))
    printUsage()
    sys.exit()

queryId = sys.argv[1]

inDir = "/u/a/d/adbhat/private/gitRepository/bigdata_cs838/results/q2"
outDir = "/u/a/d/adbhat/private/gitRepository/bigdata_cs838/processedResults/q2"

inDir_mr = os.path.join(inDir, queryId, "mr")

if (not os.path.exists(inDir)):
    print "The input folder does not exist." + inDir
    printUsage()
    sys.exit()

if not os.path.exists(outDir):
    os.makedirs(outDir)

outFile_mr_nr = os.path.join(outDir, "mr", "query" + queryId + "_" + "mr" + "_variousNR" + ".txt")
silentremove(outFile_mr_nr)
compareVaryingNumReducers(inDir_mr, outFile_mr_nr, queryId, "mr", "1")

nr = '1'
outFile_mr_pc = os.path.join(outDir, "mr", "query" + queryId + "_" + "mr" + "_nr" + str(nr) + "_variousPC" + ".txt")
silentremove(outFile_mr_pc)
compareVaryingParallelCopies(inDir_mr, outFile_mr_pc, nr, queryId, "mr", "1")

nr = '1'
pc = '15'
outFile_mr_cm = os.path.join(outDir, "mr", "query" + queryId + "_" + "mr" + "_nr" + str(nr) + "_pc" + str(pc) + "_variousCM" + ".txt")
silentremove(outFile_mr_cm)
compareVaryingCompletedMaps(inDir_mr, outFile_mr_cm, nr, pc, queryId, "mr", "1")


# inDir_tez = os.path.join(inDir, queryId, "tez")
#
# outFile_tez_cr = os.path.join(outDir, "tez", "query" + queryId + "_" + "tez" + "_variousCR" + ".txt")
# silentremove(outFile_tez_cr)
# compareVaryingContainerReuse(inDir_tez, outFile_tez_cr, queryId, "tez", "1")
#
# outFile_tez_pc = os.path.join(outDir, "tez", "query" + queryId + "_" + "tez" + "_variousPC" + ".txt")
# silentremove(outFile_tez_pc)
# cr = 'true'
# compareVaryingParallelCopies_tez(inDir_tez, "tez", outFile_tez_pc, cr, queryId, "tez", "1")
# cr = 'false'
# compareVaryingParallelCopies_tez(inDir_tez, "tez", outFile_tez_pc, cr, queryId, "tez", "1")



