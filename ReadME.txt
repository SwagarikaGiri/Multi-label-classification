step 1: run the file "tf_idf_and_output.py" it takes input file as input_genre2_formated.csv and movie_data_formated.csv
the seperator in our case is "^" for input_genre2_formated and movie_data_formated and  for rest file it is ","
input_genre2_formated.csv is a file of 10892 movie data that has only 2 label as output 
movie_data_formated.csv is the actual file with 44000 movie data that has genre of variable count
we have used movie_data_formated.csv to find all genre and we have picked only those genre that has frequency more then 1000
step2: on runing the "tf_idf_and_output.py" file u will get  normalized tf_idf of movie based on bag of words  which are tf_idf_csv_normalized.csv and output_genre2_normalized.csv  better try it in a small size i.e 1000
step3: now run the "our_model.py" it will take "tf_idf_csv_normalized.csv" file for making the training data and the testing data and "output_genre2_normaized.csv" for the label data and create 3 file one  actual output, predicted output and actual output and predicted output together seperated by "_" for creation of confusion matrix and  accuracy stuff
step 4: now run the "cal_accuracy.py"  give input the file "label_and_output_pca.csv" that has actual output and predicted output together and it gives the result file that has precision, recall, f1-score etc
"" as some file had size more than 100mb i have kept it in zipped form""
