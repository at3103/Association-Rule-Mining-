import pandas as pd
import numpy as np
from calendar import month_name, day_name 
from datetime import datetime

def pre_vectorize():
	#Give the name of your target csv file
	source = 'Data_set_50k_stratify'
	target = 'Integrated_data_set'

	#Load dataset
	dataset = pd.DataFrame.from_csv(source + '.csv')

	#Extracting the values from the dataframe
	array = dataset.values
	time_zone = {'A':'Morning',
				'B':'Noon',
				'C':'Evening',
				'D':'Night'}

	#Convert into zones and months
	for i in range(0,len(array)):
		datetime_obj = datetime.strptime(array[i][1], '%m/%d/%y %H:%M')
		array[i][1] = day_name[datetime_obj.weekday()]
		t = array[i][2].split()
		check = int(t[1] == 'PM')
		hour = int(t[0].split(':')[0])%12
		zone = time_zone[chr((hour + check * 12)/6 + 65)] 
		array[i][2] = zone

	#Save to csv file
	df = pd.DataFrame.from_records(array[:][1:])
	df.to_csv(target + '.csv')
