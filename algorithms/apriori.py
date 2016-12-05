import pandas as pd
import numpy as np
import itertools

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
				Ck[common_key] = L_k[keys[i]] + L_k[keys[j]] #Union (to subtract intersection)
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

		# for x in items.split("&&"):

		# 	if L_k.get(x,0) == 0:
		# 		#print "Here"
		# 		del Ck[items]
		# 		break
	return Ck	



min_sup = 0.01
min_conf = 0.3

source = '../Data_Set_gen/vectorized_data_set'

#Load dataset
dataset = pd.DataFrame.from_csv(source + '.csv')

#Extracting the values from the dataframe
array = dataset.values
min_sup_count = int(min_sup*len(array))
print min_sup_count
L_k = []
Li = {}
for i in range(1,len(dataset.columns)):
	if sum(array[:,i]) >= min_sup_count:
		Li[dataset.columns[i]] = sum(array[:,i])
L_k.append(Li)

#print L_k
k=1
while len(L_k[k-1])>0:
	Li = {}
	Ck = apriori_gen(L_k[k-1],k)
	#Subtracting intersection
	intersection_count=np.ones(len(array))
	#L_temp = {}
	for items in Ck.keys():
		for x in items.split("&&"):
			#if x in dataset.columns:
			column_index = dataset.columns.get_loc(x)
			intersection_count = np.logical_and(intersection_count,array[:,column_index]) 
		Ck[items] -= sum(intersection_count)		
		if Ck[items] < min_sup_count:
			del Ck[items]	
			#L_temp[items] = Ck[items]
	L_k.append(Ck)
	#print len(L_k)
	#print L_k[1]	
	k += 1	
#print k	
for i in range(len(L_k)):
	print i
	print L_k[i]
#print L_k[k-2]
#print L_k[1]

				



#dataset.columns.get_loc('1_Monday')
