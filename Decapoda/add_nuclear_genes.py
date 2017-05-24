def add_nuclear_genes(email):
	import sqlite3 as sq
	import csv
	conn = sq.connect('decapoda.db')
	c = conn.cursor()


	from Bio import Entrez, SeqIO
	Entrez.email = email
	genes = ['18S', '28S']
	count = 1
	acc_nums = []
	for gene in genes:
		f = open('decapoda_out/out'+gene+'.fasta', 'r')
		lines = f.readlines()
		print gene
		for l in range(len(lines)):
			if lines[l][0] == '>':
				print l
				line = lines[l]
				data = line.split(' ')
				acc_num = data[-1]
				words = data[:-1]
				species = ' '.join(words)
				seq = lines[l+1]
				print acc_num
				if acc_num not in acc_nums:
					acc_nums.append(acc_num)
					handle = Entrez.efetch(db="nucleotide", id=acc_num, rettype = "gb", retmode= "text")
					record = SeqIO.parse(handle, "genbank")
					r = next(record)
					try:
						x=r.annotations['references'][-1].journal
						start=x.find('(')
						end=x.find(')')
						authors = r.annotations['references'][-1].authors
						pub = x[end+2:]
						date = x[start+1:end]
					except KeyError:
						authors = ' '
						pub = ' '
						date = ' '
					c.execute("INSERT INTO Sequence_Info VALUES (?, ?, '', 'n', ?, ?, ?, ?, ?, ?)", (acc_num, seq, 'gene'+str(count), species, len(seq), authors, pub, date))
					c.execute("INSERT INTO Genes VALUES (?, ?, 'n')", ('gene'+str(count), gene))
					count += 1
				else:
					print acc_num + ' is a bad acc_num!!!'
		f.close()


	conn.commit()
	conn.close()
