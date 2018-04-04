""" we have a file that we will use for accurrary and various measures of accurracy"""
""" we need the label of genre classification that we will  use from already stored file"""
""" first we need to make the confusion matrix"""
"""we will store the corresponsing values in the dictionary"""
import csv
genre_list=['Fiction','Romance','Animation','Music','Comedy','War','Horror','Western','Thriller','Adventure','Mystery','Science','Foreign','Drama','Action','Crime','Documentary','History','Family','Fantasy']
# print genre_list
# print len(genre_list)
input_file="label_and_output_pca.csv"
delimit=","
output_csv="accuracy_measure_unnormalized.csv"
with open(output_csv,'wb') as output_csvfile:
		spamwriter = csv.writer(output_csvfile, delimiter=delimit,quotechar='|')
		col1=['Genre name','True Positive','True Negative','False Positive','False  Negative','Precision','Recall','F1-Score']
		spamwriter.writerow(col1)
		for i in range(0,20):
			print i
			list_=[]
			TP=0
			TN=0
			FP=0
			FN=0
			Precision=0
			Recall=0
			F1_score=0
			list_.append(genre_list[i])
			with open(input_file, 'rb') as input_csvfile:
				spamreader = csv.reader(input_csvfile, delimiter=delimit, quotechar='|')
				for line in spamreader:
					val=line[i]
					if val=='1_1':
						TP=TP+1
					if val=='0_1':
						FP=FP+1
					if val=='1_0':
						FN=FN+1
					if val=='0_0':
						TN=TN+1
				print genre_list[i]
				print TP
				print FP
				print TN
				print FN
				try:
					Precision=float(TP)/float(TP+FP)
				except:
					Precision=0
				try:
					Recall=float(TP)/float(TP+FN)
				except:
					Recall=0
				try:
					F1_score=float(2*Precision*Recall)/float(Precision+Recall)
				except:
					F1_score=0
				list_.append(TP)
				list_.append(TN)
				list_.append(FP)
				list_.append(FN)
				list_.append(round(Precision,2))
				list_.append(round(Recall,2))
				list_.append(round(F1_score,2))
				spamwriter.writerow(list_)


