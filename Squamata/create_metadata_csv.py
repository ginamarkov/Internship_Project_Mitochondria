# this function searches genbank using Entrez for complete squamata geones and writes their acc_num, species name, taxonomy, publication information, and the sequence itself to a csv called metadata.csv

def create_metadata_csv(email):
	import sqlite3 as sql
	import csv

	from Bio import Entrez, SeqIO
	Entrez.email = email

	handle = Entrez.esearch(db='nucleotide', retmax=1000, term='lepidosauria AND squamata AND mito* AND "complete genome" NOT ("unverified" OR partial[Title] OR incomplete OR "nearly complete" OR shotgun OR microsatellite)')

	record = Entrez.read(handle)
	ids = record["IdList"]
	acc_num = []

	dataOut = open("metadata.csv", "w")
	writeData = csv.writer(dataOut)
	headers=['acc_num', 'species', 'taxonomy', 'authors', 'journal', 'date', 'seq']
	writeData.writerow(headers)

	for i in ids:
		handle = Entrez.efetch(db="nucleotide", id=i, rettype = "gb", retmode= "text")
		record = SeqIO.parse(handle, "genbank")
		r = next(record)

		x=r.annotations['references'][-1].journal
		start=x.find('(')
		end=x.find(')')
		info=[(r.annotations['accessions'][0]),(r.annotations['source']), (r.annotations['taxonomy']), (r.annotations['references'][-1].authors), x[end+2:],x[start+1:end], r.seq]
		writeData.writerow(info)

	
	dataOut.close()
