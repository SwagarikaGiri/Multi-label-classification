""" now we have filtered the dataset according to the genre present"""
"""  we have to carry out second phase of preprocessing that is removing the stop words and steming"""

from sklearn.model_selection import train_test_split
import math
import csv
import nltk
import string
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
stop = set(stopwords.words('english'))
from nltk.tokenize import sent_tokenize, word_tokenize
ps = PorterStemmer()
dictionary=dict() # it has the total unique words
dictionary_1 = dict() # it has only those words frequency more than 10
sentence = "this is ....   a's foo bar sentence"
input_csv="input_genre2_formated.csv"
delimit="^"
train=[]
test=[]
bag_of_words=[] #unique vocabulary that will be used to make the feature vector
# it is the dictionary of line which will be newly created and destroyed with every line
def remove_stopwords_steming(sentence):
	sentence=sentence.translate(None, string.punctuation)
	string1=""
	list_=[i for i in word_tokenize(sentence.lower()) if i not in stop] 
	for i in list_:
		try:
			 value=ps.stem(i)
			 string1=string1+str(value)+" "
		except:
			pass
	return string1
def format_synopsis(input_csv,output_csv,delimit):
	with open(output_csv,'wb') as output_csvfile:
		spamwriter = csv.writer(output_csvfile, delimiter=delimit,quotechar='|')
		with open(input_csv, 'rb') as input_csvfile:
			spamreader = csv.reader(input_csvfile, delimiter=delimit, quotechar='|')
			for line in spamreader:
				string=remove_stopwords_steming(line[2])
				# print string
				spamwriter.writerow([line[0],line[1],string,line[3]])
# format_synopsis("input_genre_2.csv","input_genre2_formated.csv","^")
def create_dictionary_func(sentence):
	list_=[i for i in word_tokenize(sentence.lower())] 
	# print list_
	for ele in list_:
		if ele not in dictionary:
			dictionary[ele]=1
		else:
			dictionary[ele]=dictionary[ele]+1
	for key,value in dictionary.iteritems():
		if value > 10:
			dictionary_1[key]=value



def create_dictionary(spamreader):
	for line in spamreader:
		create_dictionary_func(line[2])

""" we have kept 80 % data for training and 20% data for testing"""
def create_training_testing(input_csv,delimit):
	train=[]
	with open(input_csv, 'rb') as input_csvfile:
			spamreader = csv.reader(input_csvfile, delimiter=delimit, quotechar='|')
			for line in spamreader:
				train.append(line)
	return train
"""we will create bag of words"""
def create_bow(lexicon):
	bow=[]
	for key,value in lexicon.iteritems():
		bow.append(key)
	return bow
""" frequency of each line"""
def frequency_line(sentence,lexicon):
	list_ele=[i for i in word_tokenize(sentence.lower())] 
	for ele in list_ele:
		if ele not in lexicon:
			lexicon[ele]=1
		else:
			lexicon[ele]=lexicon[ele]+1
	return lexicon
""" a function to calculate tf_idf"""
"""ele is the particular element of tf_idf vector, dict_line is where we can find instance frequency, D is total number of Document"""
def calculate_tf_idf(ele,dict_line,D,dictionary_1):
	document_count=D
	print ele
	if ele not in dict_line:
		instance_frequency=0.001
	else:
		instance_frequency=dict_line[ele]
	if ele not in dictionary_1:
		document_frequency=0.00
	else:
		document_frequency=dictionary_1[ele]
	print instance_frequency
	print document_frequency
	print document_count
	if document_frequency==0.00:
		return 0.00
	else:
		result=instance_frequency*(math.log10(float(document_count)/float(document_frequency)))
		return result

""" we will also have label"""
""" we will create function for tfidf"""
def create_tf_idf_matrix(train,dictionary_1,bag_of_words,output_csv,delimit,D):
	with open(output_csv,'wb') as output_csvfile:
		spamwriter = csv.writer(output_csvfile, delimiter=delimit,quotechar='|')
		count=0
		document_count=D
		col1=[]
		col1.append('tmid_id')
		for i in bag_of_words:
			col1.append(i)
		print "size of first column"
		print len(col1)
		spamwriter.writerow(col1)
		for line in train:
			string_tfidf=""
			tf_idf=[]
			dict_line=dict()#it will be created and destroyed with each line
			tf_idf.append(line[0])
			dict_line=frequency_line(line[2],dict_line)
			vector=[]
			for ele in bag_of_words:
				value = calculate_tf_idf(ele,dict_line,document_count,dictionary_1)
				vector.append(value)
				norm = [float(i)/float(max(vector)) for i in vector]
				for ele in norm:
					tf_idf.append(round(ele,5))
			print "tf_idf"
			print len(tf_idf)
			spamwriter.writerow(tf_idf)


unique_genre=dict()
genre_list=[]
eliminate_genre=[]
def read_csv_file(input_file,delimit):
	with open(input_file, 'rb') as input_csvfile:
			spamreader = csv.reader(input_csvfile, delimiter=delimit, quotechar='|')
			for line in spamreader:
				genre=line[3].split(" ")
				find_unique_genre(genre)
def find_unique_genre(list):
	for i in range(0,len(list)):
		if list[i]!='':
			if list[i] not in unique_genre:
				unique_genre[list[i]]=1
			else:
				unique_genre[list[i]]=unique_genre[list[i]]+1
def filter_low_freq(lexicon):
	genre_list=[]
	eliminate_genre_list=[]
	for key,value in lexicon.iteritems():
		if (value>1000):
			genre_list.append(key)
		else:
			eliminate_genre_list.append(key)
	return genre_list,eliminate_genre_list
def create_vector(movie_list,genre_list):
	vector=[]
	list_=[i for i in word_tokenize(movie_list)] 
	for ele in genre_list:
		if ele in list_:
			vector.append(1)
		else:
			vector.append(0)
	print len(vector)
	return(vector)

def create_output(train,genre_list,output_csv,delimit):
	with open(output_csv,'wb') as output_csvfile:
		spamwriter = csv.writer(output_csvfile, delimiter=delimit,quotechar='|')
		col1=[]
		col1.append('tmid_id')
		for i in genre_list:
			col1.append(i)
		spamwriter.writerow(col1)
		for line in train:
			vector=[]
			vector.append(line[0])
			vector_list=create_vector(line[3],genre_list)
			for i in vector_list:
				vector.append(i)
			spamwriter.writerow(vector)





read_csv_file('movie_data_formated.csv','^')
genre_list,eliminate_genre=filter_low_freq(unique_genre)
print genre_list
print len(genre_list)
print eliminate_genre
print len(eliminate_genre)
train=create_training_testing(input_csv,delimit)
# train=train[0:1000]
output_csv_="output_genre2_normalized.csv"
delimit_=","
create_output(train,genre_list,output_csv_,delimit_)
create_dictionary(train)
D=len(train)
bag_of_words=create_bow(dictionary_1)
create_tf_idf_matrix(train,dictionary_1,bag_of_words,"tf_idf_csv_normalized.csv",",",D)


			
