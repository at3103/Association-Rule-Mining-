import pandas as pd
import numpy as np
import sklearn
from sklearn import model_selection



#Load dataset
url = "Top_5_2015.csv"
dataset = pd.read_csv(url)


#Extracting the values from the dataframe
array = dataset.values
print array[0][0:5]
#Separating the features and the labels
X = array [:,0:5]
Y = array[:,5:6]
print Y[0]


#Validation Size
test_size = 0.01

#Set the seed for randomness here
seed = 7

#Obtain the training and test sets
X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X, Y,
 	test_size = test_size, random_state = seed)

t = np.concatenate((X_test,Y_test),axis=1)
df = pd.DataFrame.from_records(t)
df.to_csv('Data_set.csv')

