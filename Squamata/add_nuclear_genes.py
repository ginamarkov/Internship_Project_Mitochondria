
# this function adds all of the nuclear genes to the database (all of the other genes have been mitochondrial genes)

def add_nuclear_genes(email):
	import sqlite3 as sq
	import csv
	conn = sq.connect('squamata.db')
	c = conn.cursor()


	from Bio import Entrez, SeqIO
	Entrez.email = email

	# standardizes each gene name
	genes = ['SCN4a', 'PRLR', 'rhodopsin_gene', 'alpha-enolase', 'PLA2', 'PNN', 'PTGER4', 'NGFB', '18S', 'DNAH3', 'BMP2', 'MKL1', 'SLC30A1', 'TRAF6', 'ZEB2', 'FSHR', 'SLC8A1', 'ZFP36L1', 'FSTL5', 'GPR37', 'LRRN1', 'AHR', 'CAND1', 'ENC1', 'HOXA13', 'VCPIP1', '28S', 'DLL', 'MC1R', 'PDC', 'ADNP', 'GAPD', 'AMEL', 'NT3', 'RAG2', 'SINCAIP', 'RAG1', 'ACM4', 'BDNF', 'CMOS', 'KIF24', 'ECEL', 'R35', 'PTPN']
	count = 1
	acc_nums = []

	# loops through the files in the squamata_out file, which contains the best sequences for each gene. Accesses genbank to pull information about the publication information, sequence, and other information necessary for the Sequence_Info table. 
	for gene in genes:
		f = open('squamata_out/out'+gene+'.fasta', 'r')
		lines = f.readlines()

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

					# populates the Sequence_Info table with information about the nuclear genes
					c.execute("INSERT INTO Sequence_Info VALUES (?, ?, '', 'n', ?, ?, ?, ?, ?, ?)", (acc_num, seq, 'gene'+str(count), species, len(seq), authors, pub, date))

					# populates the Genes table with the gene ID, gene name, and type of gene (nuclear)
					c.execute("INSERT INTO Genes VALUES (?, ?, 'n')", ('gene'+str(count), gene))
					count += 1
				else:
					print acc_num + ' is a bad acc_num!!!'
		f.close()


	conn.commit()
	conn.close()

