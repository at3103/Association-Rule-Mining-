import pandas as pd
import numpy as np
import itertools
from datetime import datetime
from utils.display import *

def apriori_gen(L_k,k):
	Ck = {}
	keys = L_k.keys()
	for i in range(len(keys)):
		for j in range(i+1,len(keys)):
			c = 0
			temp = keys[i].split("&&")
			temp1 = keys[j].split("&&")			
			for ele in temp:
				if ele in temp1:
					c += 1	
			if c == k-1:
				c_temp = list(set(temp+temp1))	
				common_key = '&&'.join(c_temp)
				Ck[common_key] = 0


	# PRUNE STEP
	for items in Ck.keys():
		# List with items 
		key = items.split("&&") 

		 # Generating subset of key list
		subsets = list(set(itertools.combinations(key,k)))
		for ele in subsets:
			subset_key = '&&'.join(ele)
			if L_k.get(subset_key,0) == 0:
				del Ck[items]
				break
	return Ck	


def apriori(min_sup, min_conf, choice, verbose):

	print "\nAlgorithm Started", datetime.now().time(), "\n"
	source = 'Data_Set_gen/vectorized_data_set'
	L_k = []
	Li = {}

	#Load dataset
	dataset = pd.DataFrame.from_csv(source + '.csv')

	#Extracting the values from the dataframe
	array = dataset.values

	min_sup_count = int(min_sup*len(array))
	print "Minimum support is ",min_sup, " which is ", min_sup_count
	print "Minimum confidence is ",min_conf, " which is ", min_conf * 100.0

	for i in range(1,len(dataset.columns)):
		if sum(array[:,i]) >= min_sup_count:
			Li[dataset.columns[i]] = sum(array[:,i])
	L_k.append(Li)

	k=1
	while len(L_k[k-1])>0:
		Li = {}
		Ck = apriori_gen(L_k[k-1],k)

		for items in Ck.keys():
			intersection_count=np.ones(len(array))

			for x in items.split("&&"):
				column_index = dataset.columns.get_loc(x)
				intersection_count = np.logical_and(intersection_count,array[:,column_index]) 
			Ck[items] += sum(intersection_count)
	
			if Ck[items] < min_sup_count:
				del Ck[items]	
		L_k.append(Ck)
		k += 1	

	#Printing Frequent itemsets	
	display(L_k, len(array), min_sup, 0)

	Columns_dict = {'1': 'Day is ',
					'2': 'Time of the day is ',
					'3': 'Agency is ',
					'4': 'The inquiry is ',
					'5': 'Call resolution is '
	}

	rules =[]
	required_rhs=[]
	
	if choice:
		for items in L_k[0].keys():
			if '5_' in items:
				required_rhs.append(items)

	rhs = {'0': L_k[0].keys(),
		   '1': required_rhs}

	for items in rhs[str(choice)]:
		for i in range(0,len(L_k)-1):
			for itemsets in L_k[i].keys():
				numer = 0
				confidence = 0

				if L_k[i+1].get((itemsets + "&&" + items),0) != 0:
					numer = L_k[i+1][(itemsets + "&&" + items)]
				elif L_k[i+1].get((items + "&&" + itemsets),0) != 0:
					numer = L_k[i+1][(items + "&&" + itemsets)]

				if numer:
					confidence = float(numer)/(L_k[i][itemsets])
				if confidence >= min_conf:
					rules.append([(itemsets, items),confidence, numer])

	#Printing High Confidence Rules
	display(rules, len(array), min_conf, 1)


	#Print Verbose
	if verbose:
		with open ('verbose_output.txt', 'w') as file:
			print_string = "\nVerbose Output\n"
			print_string += "\n==High-confidence association rules==(min_conf = "+ str(min_conf*100) + "%)==\n"
			print print_string
			file.write(print_string)
			for rule in rules:
				list_rules = rule[0][0].split('&&')
				for i in range(len(list_rules)):
					lhs = list_rules[i]
					index,name = lhs.split('_')
					list_rules[i] =  Columns_dict[index] + name 
				tuple_ele_one = str(' and '.join(list_rules))
				index,name = rule[0][1].split('_')
				tuple_ele_two = Columns_dict[index] + name 
				rule[0] = tuple([tuple_ele_one,tuple_ele_two])
				sup = float(rule[2]*100.0/len(array))
				print_string = rule[0][0] + " ===>  " + rule[0][1] + " with confidence : " + str(rule[1]) + " and support:" + str(sup) + "\n"
				print print_string
				file.write(print_string+"\n")

		
	print "Algorithm Complete", datetime.now().time()
