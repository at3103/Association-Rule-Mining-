import pandas as pd
import numpy as np
import itertools
from datetime import datetime

def apriori_gen(L_k,k):
	Ck = {}
	keys = L_k.keys()
	for i in range(len(keys)):
		for j in range(i+1,len(keys)):
			c = 0
			temp = keys[i].split("&&")
			temp1 = keys[j].split("&&")			
			for ele in temp:
				if ele in keys[j]:
					c += 1	
			if c == k-1:
				c_temp = list(set(temp+temp1))	
				common_key = '&&'.join(c_temp)
				Ck[common_key] = 0#L_k[keys[i]] + L_k[keys[j]] #Union (to subtract intersection)

	print k, "-item set Apriori C_k generation complete", datetime.now().time()
	print "Size of", k ,"-item set before pruning", len(Ck)
	# for item1 in L_k.keys():						 	
	# 		for ele in temp:
	# 			if ele in keys[j]:
	# 				common_key = keys[i]+'&&'+keys[j].strip('&&'+ele)
	# 				Ck[common_key] = L_k[keys[i]] + L_k[keys[j]] #Union (to subtract intersection)
	# # for item1 in L_k.keys():
	# 	for item2 in set(L_k.keys())-{item1}:
	# 		Ck[item1+"&&"+item2] = L_k[item1] + L_k[item2]

	# PRUNE STEP
	#print Ck.keys()
	for items in Ck.keys():
		key = items.split("&&") # List with items 
		subsets = list(set(itertools.combinations(key,k))) # Generating subset of key list
		#print "Subsets!"
		#print subsets
		for ele in subsets:
			subset_key = '&&'.join(ele)
			if L_k.get(subset_key,0) == 0:
				del Ck[items]
				break
	print k, "-item set Apriori pruning complete", datetime.now().time()
	print "Size of", k ,"-item set after pruning", len(Ck)
		# for x in items.split("&&"):

		# 	if L_k.get(x,0) == 0:
		# 		#print "Here"
		# 		del Ck[items]
		# 		break
	return Ck	



min_sup = 0.005
min_conf = 0.3

source = '../Data_Set_gen/vectorized_data_set'

#Load dataset
dataset = pd.DataFrame.from_csv(source + '.csv')

#Extracting the values from the dataframe
array = dataset.values
min_sup_count = int(min_sup*len(array))
print "Min Support Count: ", min_sup_count

L_k = []
Li = {}
for i in range(1,len(dataset.columns)):
	if sum(array[:,i]) >= min_sup_count:
		Li[dataset.columns[i]] = sum(array[:,i])
L_k.append(Li)
print "First item set complete", datetime.now().time()
print "Size of 1-item setm", len(L_k[0])
#print L_k

k=1
while len(L_k[k-1])>0:
	Li = {}
	Ck = apriori_gen(L_k[k-1],k)
	#Subtracting intersection
	#L_temp = {}
	for items in Ck.keys():

		intersection_count=np.ones(len(array))
		
		for x in items.split("&&"):
			#if x in dataset.columns:
			column_index = dataset.columns.get_loc(x)
			intersection_count = np.logical_and(intersection_count,array[:,column_index]) 
		Ck[items] += sum(intersection_count)		
		if Ck[items] < min_sup_count:
			del Ck[items]	
			#L_temp[items] = Ck[items]
	L_k.append(Ck)
	print k+1, "th item set complete", datetime.now().time()
	print "Size of", k,"-item setm", len(L_k[k])
	#print len(L_k)
	#print L_k[1]	
	k += 1	
print k+1, "th item set complete", datetime.now().time()	

total_length = 0

for i in range(len(L_k)):
	print i
	print L_k[i]
	print "Number of", i+1, "-item set is", len(L_k[i])
	total_length += len(L_k[i])
#print L_k[k-2]
#print L_k[1]

Columns_of_dataset = [0] * 6
for items in L_k[0].keys():
	index,item = items.split('_')
	Columns_of_dataset[index].append(item)
rules =[]
for items in L_k[0].keys():
	for i in range(1,len(L_k)):
		for itemsets in L_k[i].keys():
			#key_itemset = itemsets.keys()
			if L_k[i+1].get((itemsets + "&&" + items),0) != 0:
				numer = L_k[i+1][(itemsets + "&&" + items)]
			elif L_k[i+1].get((items + "&&" + itemsets),0) != 0:
				numer = L_k[i+1][(items + "&&" + itemsets)]
			else:
				numer = 0
			confidence = numer/(L_k[i+1])
			if confidence >= min_conf:
				rules.append([(L_k[i+1], items),confidence])







print "Complete", datetime.now().time(), "Total number of k item sets", total_length
				
#dataset.columns.get_loc('1_Monday')

