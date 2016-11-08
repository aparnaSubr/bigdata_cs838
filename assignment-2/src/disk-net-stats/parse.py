import sys

fd = open(sys.argv[1], 'r')
lines = fd.readlines()
lines = [line.strip() for line in lines if not line.strip() == ''] 

netrx = lines[:6]
netrx = [line.split(' ') for line in netrx if len(line.split(' ')) == 2]
vals = [int(rx[0]) - int(rx[1]) for rx in netrx]
print('Network Rx {0}'.format(sum(vals)))

nettx = lines[6:12]
nettx = [line.split(' ') for line in nettx if len(line.split(' ')) == 2]
vals = [int(tx[0]) - int(tx[1]) for tx in nettx]
print('Network Tx {0}'.format(sum(vals)))

diskr = lines[12:18]
diskr = [line.split(' ') for line in diskr if len(line.split(' ')) == 2]
vals = [int(tx[0]) - int(tx[1]) for tx in diskr]
print('Disk Read {0}'.format(sum(vals)))

diskw = lines[18:]
diskw = [line.split(' ') for line in diskw if len(line.split(' ')) == 2]
vals = [int(tx[0]) - int(tx[1]) for tx in diskw]
print('Disk Write {0}'.format(sum(vals)))

