
# this function creates the csv that will be used to populate the MitoGeneLocation table in the database. 
def create_mitogeneloc():
	import csv
	import re
	import sqlite3 as sq
	conn = sq.connect("squamata.db")
	c=conn.cursor()

	# mitogenelocation table contains 'acc_num', 'gene_ID', 'sequence', 'length', 'start', 'end', 'orientation', sign 
	
	genesin=open('geneposition.csv', 'r') #contains acc_num, gene, location
	out = open('mitogene_location.csv', 'w') #to be imported into sql

	write = csv.writer(out)
	read = csv.reader(genesin)

	#accnnum taken from geneposition, assign gene_ID, sequence is spliced

	read.next()

	# splices the full genome sequence at the start and end position for each gene. Finds the length of each genetic sequence. 

	for line in read:
		
		acc_num=line[0]
		o=line[2][line[2].find(")")-1]
		locs = []
		s1=''
		s2=''
		sign=None
		for col, s, e in zip(re.finditer(":", line[2]), re.finditer('\[', line[2]), re.finditer('\]', line[2])):
			colon=col.start()
			end_loc = e.start()
			start = line[2][s.start()+1:colon]
			end = line[2][colon+1:end_loc]


			if '<' in start:
				start=start[1:]
				sign = '<start'
			elif '>' in end:
				end = end[1:]
				sign = '>end'
			locs.append([start,end])


		for l, s in zip(locs, [s1, s2]):
			for a in c.execute ("SELECT Sequence_Info.sequence from Sequence_Info where Sequence_Info.acc_num = (?);", (acc_num,)):
				s1=a[0][int(locs[0][0]):int(locs[0][1])]
				if len(locs)==2:
					s2=a[0][int(locs[1][0]):int(locs[1][1])]

		seq=s1+s2
		length=len(seq)
		gene_name=line[1]
		
		write.writerow([acc_num, gene_name, seq, length, start, end, o, sign])	

	genesin.close()
	out.close()


