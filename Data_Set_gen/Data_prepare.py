import pandas as pd
import numpy as np
from sklearn import model_selection
from pre_vectorizing import *
from vectorizing import *

#Give the name of your target csv file
source = 'Top_5_2015'
target = 'Data_set_50k_stratify'

#Load dataset
dataset = pd.read_csv(source + '.csv')

#Set the number of features
number_of_features = 6
label_start = (number_of_features-1)
label_end   = number_of_features

#Extracting the values from the dataframe
array = dataset.values

#Validation Size
test_size = 0.1

#Separating the features and the labels
X = array [:,0:(number_of_features-1)]
Y = array[:,label_start:label_end]

#Set the seed for randomness here
seed = 17

#Obtain the training and test sets
X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X, Y,
 	test_size = test_size, random_state = seed, stratify = Y)

#Save to csv file
t = np.concatenate((X_test,Y_test),axis=1)
df = pd.DataFrame.from_records(t)
df.to_csv(target + '.csv')

pre_vectorize()
vectorize()

