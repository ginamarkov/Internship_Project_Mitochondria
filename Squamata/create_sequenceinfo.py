# this function creates a csv called sequence_info. This csv contains the information in clean metedata, but it is cleaned up a little to get rid of unnecessary spaces and parenthesis. The information in sequence_info.csv is ready to be put in the database.

def create_sequenceinfo():
	import csv
	datain = open('cleanmetadata.csv', 'r')
	dataout = open('sequence_info.csv', 'w')
	read = csv.reader(datain)
	write = csv.writer(dataout)

	read.next()

	for line in read:
		if "(" in line[1]:
			end = line[1].find('(')
		else:
			end = len(line[1])
		l = line[1][14:end]
		while l[-1] == ' ':
			l = l[:-1]
		write.writerow([line[0], line[-1], 'm', None, l, len(line[-1]), line[3], line[4], line[5]])


	datain.close()
	dataout.close()