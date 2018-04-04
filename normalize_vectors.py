"""we need to normalize the vectors that will be used for training and testing"""
import csv
import pandas as pd
""" we now need a testing dataset that we have in another csv file"""
input_file="tf_idf_csv.csv"
delimit=","
output_csv="tf_idf_csv_normalized.csv"
with open(output_csv,'wb') as output_csvfile:
		spamwriter = csv.writer(output_csvfile, delimiter=delimit,quotechar='|')
		with open(input_file, 'rb') as input_csvfile:
			spamreader = csv.reader(input_csvfile, delimiter=delimit, quotechar='|')
			count=0
			for line in spamreader:
				print count
				list_=[]
				count=count+1
				if(count==1):
					spamwriter.writerow(line)
				else:
					list_.append(line[0])
					line_=line[1:]
					vector=[float(i) for i in line_]
					for i in vector:
						val=float(i)/float(max(vector))
						list_.append(round(val,5))
					spamwriter.writerow(list_)
			

		