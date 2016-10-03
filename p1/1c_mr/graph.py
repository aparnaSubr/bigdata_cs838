import re 
import sys
import matplotlib.pyplot as plt
import os
import fnmatch

output_dir = "graphs/"
matches = []
for root, dirnames, filenames in os.walk(sys.argv[1]): # intermediate_files
    for filename in fnmatch.filter(filenames, '*.txt'):
        matches.append(os.path.join(root, filename))

for filename in matches:
	print(filename);
	hand=open(filename);
	all_line=-1;
	map_line=-1;
	reduce_line=-1;
	end_line=-1;
	index=1;
	for line in hand:
		if(line.startswith('All data')):
			all_line=index
		if(line.startswith('Map data')):
			map_line=index
		if(line.startswith('Reduce data')):
			reduce_line=index
		if(line.startswith('Total Maps:')):
			end_line=index
		index=index+1;

	if(all_line==-1 or map_line==-1 or reduce_line==-1 or end_line==-1):
		print("Error in parsing");
		exit

	all_data=[]
	map_data=[]
	reduce_data=[]

	hand=open(filename);
	index=1;
	for line in hand:
		if(index>all_line and index<map_line):
			all_data.append(int(line))
		elif(index>map_line and index<reduce_line):
			map_data.append(int(line))
		elif(index>reduce_line and index<end_line):
			reduce_data.append(int(line))
		index=index+1;

	#Plotting
	x_axis=range(1,len(all_data)+1)
	
	plt.gca().set_color_cycle(['red', 'green', 'blue'])
	plt.plot(x_axis,all_data,'|',linewidth=2,linestyle='-')
	plt.plot(x_axis,map_data,'',linewidth=1,linestyle='-')
	plt.plot(x_axis,reduce_data,'',linewidth=1,linestyle='-')
	plt.legend(['reducers+maps', 'maps', 'reducers'], loc='upper right')
	#plt.show()
	
	filename=filename.split("/")
	filename=((filename[-1]).split("."))[0]
	print filename
	
	plt.title(filename)
	

	plt.savefig((output_dir+filename),bbox_inches='tight')
	plt.clf()
