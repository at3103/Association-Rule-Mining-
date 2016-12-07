import pandas as pd
import numpy as np
from datetime import datetime

#Function to vectorize the Integrated_data_set.csv and save the vectorized data in vectorized_data_set.csv
def vectorize(source):

	print "\nVectorizing Data", datetime.now().time(), "\n"

	#Name of target csv file
	target = 'Data_Set_gen/vectorized_data_set'

	#Load dataset
	dataset = pd.DataFrame.from_csv(str(source))

	#Extracting the values from the dataframe
	array = dataset.values
	df = pd.DataFrame.from_records(array)

	#Save to csv file
	gt = pd.get_dummies(df)
	gt.to_csv(target + '.csv')

	print "\nDone with vectorizing", datetime.now().time(), "\n"
