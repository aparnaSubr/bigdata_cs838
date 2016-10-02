import sys, os, os.path, getpass, tarfile, glob, shutil, commands, re


def printUsage():
    print "Usage: python processTry.py <queryId> <Trial> <Type>"


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
            outLines += inLine.split(", ")[0].replace(":", ":\t").replace(" seconds", "\tseconds") + "\n"
            outLines += inLine.split(", ")[1].replace(":", ":\t").replace(" row", "\trow") + "\n"
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
                innerDict = {"read": fragments[5], "write": fragments[9]}
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
    diffDiskBytes['sda1']['write'] = (
                                         int(afterDiskBytes['sda1']['write']) - int(
                                             beforeDiskBytes['sda1']['write'])) * 512

    diffDiskBytes['sdb1']['read'] = (int(afterDiskBytes['sdb1']['read']) - int(beforeDiskBytes['sdb1']['read'])) * 512
    diffDiskBytes['sdb1']['write'] = (
                                         int(afterDiskBytes['sdb1']['write']) - int(
                                             beforeDiskBytes['sdb1']['write'])) * 512

    diffDiskBytes['sdc1']['read'] = (int(afterDiskBytes['sdc1']['read']) - int(beforeDiskBytes['sdc1']['read'])) * 512
    diffDiskBytes['sdc1']['write'] = (
                                         int(afterDiskBytes['sdc1']['write']) - int(
                                             beforeDiskBytes['sdc1']['write'])) * 512

    # debug
    # print "Diff DiskStats\n" + str(diffDiskBytes)
    return diffDiskBytes


if (len(sys.argv) != 4):
    print("Not enough arguments: " + str(len(sys.argv)))
    printUsage()
    sys.exit()

queryId = sys.argv[1]
trialNum = sys.argv[2]
type = sys.argv[3]

inDir = "/u/a/d/adbhat/private/gitRepository/bigdata_cs838/results/"
outDir = "/u/a/d/adbhat/private/gitRepository/bigdata_cs838/processedResults/q1"

inDir = os.path.join(inDir, queryId, type, "try_" + trialNum)
outFile = os.path.join(outDir, "query" + queryId + "_" + type + ".txt")

if (not os.path.exists(inDir)):
    print "The input folder does not exist." + inDir
    printUsage()
    sys.exit()

if not os.path.exists(outDir):
    os.makedirs(outDir)

print "\ninDir: " + inDir

slaveDirNames = ["master", "slave2", "slave3", "slave4"]

lines = "Query" + queryId + "\t" + type + "\ttrial" + trialNum +"\n"

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
lines += "eth0 rx\teth0 tx\tlo rx\tlo tx\n"
lines += str(totNetStats['eth0']['rx']) + "\t" + str(totNetStats['eth0']['tx']) + "\t" + str(
    totNetStats['lo']['rx']) + "\t" + str(totNetStats['lo']['tx'])
lines += "\n"
lines += "\nTotalDiskStats\n"
lines += "Read\tWrite\n"
lines += str(totDiskStats['read']) + "\t" + str(totDiskStats['write']) +"\n"

print "\n\nOutput\n" + lines


with open(outFile, "a") as myfile:
    myfile.write(lines)



# Read
# 86016+49168384+1840484352+
# 2302431232+49152+73060352+
# 86016+48455680+2329804800+
# 1228705792+73728+55001088
