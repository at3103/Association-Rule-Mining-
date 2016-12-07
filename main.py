from algorithms.apriori import *
import sys
import os
from Data_Set_gen.vectorizing import *
from datetime import datetime

# Preliminary Checks
if len(sys.argv) < 4:
	print "Please use the format: python main.py <Integrated data set> <minimum support> <minimum confidence> [v] [r]"
	exit()

integrated_dataset = str(sys.argv[1])
if os.path.isfile('Data_Set_gen/' + integrated_dataset) == 0:
	print "Please specify a valid file (Integrated_Dataset.csv)"
	exit()

min_sup = float(sys.argv[2])
min_conf = float(sys.argv[3])

if min_sup > 1 or min_sup < 0:
	print "Please specify a valid support value between 0 and 1"
	exit()

if min_conf > 1 or min_conf < 0:
	print "Please specify a valid confidence value between 0 and 1"
	exit()

# Data Vectorization
vectorize(str('Data_Set_gen/' + integrated_dataset))

#choice = 0 --> all rules | choice = 1 --> only call resolution on the right hand side
choice = 0
verbose = 0

if len(sys.argv) > 4:
	if str(sys.argv[-1]) == 'v' or str(sys.argv[-2]) == 'v':
		verbose = 1
	if str(sys.argv[-1]) == 'r' or str(sys.argv[-1]) == 'r':
		choice = 1

# Call to Apriori
apriori(min_sup,min_conf,choice,verbose)