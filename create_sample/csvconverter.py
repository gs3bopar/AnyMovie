import re

def convert2csv(name):
	tn = name + '.tsv'
	cn = name + '.csv'
	with open(tn, 'r', encoding = 'utf-8') as myfile:
		with open(cn, 'w', encoding = 'utf-8') as csv_file:
			for line in myfile:
				fileContent = re.sub("\t", ",", line)
				csv_file.write(fileContent)
	
convert2csv('title.ratings')
convert2csv('title.basics')
convert2csv('title.principals')
convert2csv('name.basics')
convert2csv('title.ratings')