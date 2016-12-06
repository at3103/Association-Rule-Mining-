from algorithms.apriori import *
from Data_Set_gen.Data_prepare import *
import sys
#Data_prepare()
if len(sys.argv) != 4:
	print "Please use the format: python main.py <Integrated data set> <minimum support> <minimum confidence>"
	exit()
integrated_dataset = sys.argv[1]
min_sup = float(sys.argv[2])
min_conf = float(sys.argv[3])

if min_sup > 1 or min_sup < 0:
	print "Please specify a valid support value between 0 and 1"
	exit()

if min_conf > 1 or min_conf < 0:
	print "Please specify a valid confidence value between 0 and 1"
	exit()

#choice = 0 --> all rules | choice = 1 --> only call resolution on the right hand side
choice = 0
apriori(min_sup,min_conf,choice)