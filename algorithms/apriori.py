import pandas as pd
import numpy as np
import itertools
from datetime import datetime
from utils.display import *

#Generating Candidate Sets and Pruning them
def apriori_gen(L_k,k):
	Ck = {}
	keys = L_k.keys()
	# Joining L_k-1 with itself
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

	# PRUNE STEP - This is to check if all possible combinations of the subset of items in Ck is present in the previous large itemset L_k-1, 
   	# Items which do not satisfy this condition are removed from the dictionary.
	for items in Ck.keys():
		# List with items 
		key = items.split("&&") 
		# Generating subset of key list
		subsets = list(set(itertools.combinations(key,k)))
		for ele in subsets:
			subset_key = '&&'.join(ele)
			# If the subset is not present in the previous Large Itemset then delete from candidate itemset
			if L_k.get(subset_key,0) == 0:
				del Ck[items]
				break
	return Ck	


def apriori(min_sup, min_conf, choice, verbose):

	print "\nAlgorithm Started", datetime.now().time(), "\n"
	source = 'Data_Set_gen/vectorized_data_set'
	L_k = []
	Li = {}

	# Load dataset
	dataset = pd.DataFrame.from_csv(source + '.csv')

	# Extracting the values from the dataframe
	array = dataset.values

	min_sup_count = int(min_sup*len(array))
	print "Minimum support is ",min_sup, " which is ", min_sup_count
	print "Minimum confidence is ",min_conf, " which is ", min_conf * 100.0

	# Generating L1 i.e 1-k Large Itemset with support
	for i in range(1,len(dataset.columns)):
		# Checking if support of the item is greater than minimum support
		if sum(array[:,i]) >= min_sup_count:
			Li[dataset.columns[i]] = sum(array[:,i])
	L_k.append(Li)

	k=1
	while len(L_k[k-1])>0:
		Li = {}
		# Call to generate Candidate Itemset
		Ck = apriori_gen(L_k[k-1],k)

		# Calculating support values for the Candidate Itemsets
		for items in Ck.keys():
			intersection_count=np.ones(len(array))

			for x in items.split("&&"):
				column_index = dataset.columns.get_loc(x)
				intersection_count = np.logical_and(intersection_count,array[:,column_index]) 
			Ck[items] += sum(intersection_count)

			# Retaining only those items whose support is greater than minimum support 
			if Ck[items] < min_sup_count:
				del Ck[items]	
		L_k.append(Ck)
		k += 1	

	# Call to print Frequent itemsets
	display(L_k, len(array), min_sup, 0)

	# Rule Generation

	rules =[]
	required_rhs=[]
	
	# Choice represents whether rule generation is retricted or not
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

				# Calculation confidence as conf(LHS=>RHS) = sup(LHS U RHS)/sup(LHS)	
				if numer:
					confidence = float(numer)/(L_k[i][itemsets])

				# Only retaining those rules whose confidence is greater than minimum confidence	
				if confidence >= min_conf:
					rules.append([(itemsets, items),confidence, numer])

	#Print Verbose
	display(rules, len(array), min_conf, verbose + 1)
		
	print "\nAlgorithm Complete", datetime.now().time()
