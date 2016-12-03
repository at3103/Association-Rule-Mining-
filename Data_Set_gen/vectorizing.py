import pandas as pd
import numpy as np

#Give the name of your target csv file and source
source = 'modified'
target = 'vector'

#Load dataset
dataset = pd.DataFrame.from_csv(source + '.csv')

#Extracting the values from the dataframe
array = dataset.values
df = pd.DataFrame.from_records(array)

#Save to csv file
gt = pd.get_dummies(df)
gt.to_csv(target + '.csv')

