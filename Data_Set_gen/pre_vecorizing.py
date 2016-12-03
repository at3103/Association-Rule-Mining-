import pandas as pd
import numpy as np
from calendar import month_name 

#Give the name of your target csv file
source = 'Data_set_50k'
target = 'modified'

#Load dataset
dataset = pd.DataFrame.from_csv(source + '.csv')

#Extracting the values from the dataframe
array = dataset.values
print len(array)

#Convert into zones and months
for i in range(0,len(array)):
	array[i][1] = month_name[int(array[i][1].split('/')[0])]
	t = array[i][2].split()
	check = int(t[1] == 'PM')
	hour = int(t[0].split(':')[0])%12
	zone = (hour + check * 12)/6 + 65 
	array[i][2] = chr(zone)

#Save to csv file
df = pd.DataFrame.from_records(array[:][1:])
df.to_csv(target + '.csv')
