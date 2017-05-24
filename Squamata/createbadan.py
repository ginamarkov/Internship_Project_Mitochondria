# this function searches genbank for squamata genomic sequences. It creates a csv with the accession numbers that were read by genbank, improved, and turned into reference sequences with new accession numbers. The refseqs are kept, while the accession numbers from the old sequences are written to a file called badan.csv

def createbadan(email):
	import csv
	f = open("badan.csv", "w")
	data = csv.writer(f)

	from Bio import Entrez, SeqIO
	Entrez.email = email

	handle = Entrez.esearch(db='nucleotide', retmax=1000, term='lepidosauria AND squamata AND mito* AND "complete genome" NOT ("unverified" OR partial OR incomplete OR "nearly complete" OR shotgun OR microsatellite)')

	data.writerow(["bad acc_nums"])

	record = Entrez.read(handle)
	ids = record["IdList"]


	for i in ids:
		handle = Entrez.efetch(db="nucleotide", id=i, rettype = "gb", retmode= "text")
		record = SeqIO.parse(handle, "genbank")
		r = next(record)
		try:
			if "reference sequence is identical to" in r.annotations['comment']:
				comm = r.annotations['comment']
				start = comm.find('reference sequence is identical to ')+35
				bad = comm[start:start+8]
				data.writerow([bad])
			elif "reference sequence was derived from" in r.annotations['comment']:
				comm = r.annotations['comment']
				start = comm.find('reference sequence was derived from ')+36
				bad = comm[start:start+8]
				data.writerow([bad])
		except KeyError:
			pass

	f.close()