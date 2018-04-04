# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from sklearn.decomposition import PCA
import keras
import heapq
import csv
y_pred_vec=[]
def label_output_vector(y_test,y_pred,output_csv,delimit):
	with open(output_csv,'wb') as output_csvfile:
		spamwriter = csv.writer(output_csvfile, delimiter=delimit,quotechar='|')
		loop1=len(y_test)
		loop2=len(y_test[0])
		for i in range(0,loop1):
			vector=[]
			for j in range(0,loop2):
				val=str(y_test[i][j])+"_"+str(y_pred[i][j])
				vector.append(val)
			spamwriter.writerow(vector)


def create_output_vector(output_data,output_csv,delimit,y_pred_vec):
	with open(output_csv,'wb') as output_csvfile:
		spamwriter = csv.writer(output_csvfile, delimiter=delimit,quotechar='|')
		for i in range(0,len(output_data)):
			max1,max2=heapq.nlargest(2, output_data[i])
			vector=[]
			y_pred_vec.append([])
			for ele in output_data[i]:
				if ((ele == max1) or(ele==max2)):
					vector.append(1)
				else:
					vector.append(0)
			y_pred_vec[i]=vector
			spamwriter.writerow(vector)
		return y_pred_vec

def create_output_label(output_label,output_csv,delimit):
	with open(output_csv,'wb') as output_csvfile:
		spamwriter = csv.writer(output_csvfile, delimiter=delimit,quotechar='|')
		for i in range(0,len(output_label)):
			spamwriter.writerow(output_label[i])

# Importing the dataset
dataset = pd.read_csv('tf_idf_csv_normalized.csv')
"""here is the training dataset"""
train = dataset.iloc[0:,1:].values
""" we now need a testing dataset that we have in another csv file"""
labelset = pd.read_csv('output_genre2.csv')
label = labelset.iloc[0:,1:].values

X_train, X_test, y_train, y_test = train_test_split(train,label,test_size = 0.2)
# Feature Scaling

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
# Make an instance of the Model here 95 % variance is retained
pca = PCA(.95)
X_train = pca.fit_transform(X_train)
X_test= pca.transform(X_test)
input_size=len(X_train[0])
print input_size
# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Dense
#Initializing Neural Network
classifier = Sequential()
# Adding the input layer and the first hidden layer
classifier.add(Dense(output_dim = 50, kernel_initializer = 'uniform', activation = 'sigmoid', input_dim = input_size))
# Adding the second hidden layer
classifier.add(Dense(output_dim = 150, kernel_initializer = 'uniform', activation = 'sigmoid'))
# Adding the output layer
classifier.add(Dense(output_dim = 20, kernel_initializer = 'uniform', activation = 'sigmoid'))
# Compiling Neural Network
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
# Fitting our model 
classifier.fit(X_train, y_train, batch_size = 10, nb_epoch = 100)
# Predicting the Test set results
y_pred = classifier.predict(X_test)
# always run them together
create_output_label(y_test,"output_label_pca_normalized.csv",",")
y_pred_vec=create_output_vector(y_pred,"output_vector_pca_normalized.csv",",",y_pred_vec)
# print y_pred_vec
#we need both the output vector and the label dataset
label_output_vector(y_test,y_pred_vec,"label_and_output_pca_normalized.csv",",")

print input_size