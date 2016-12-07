
def display(L_k):
	common_dict = {}
	
	for itemset in L_k:
		common_dict.update(itemset)
	print "2. Total_length: ", len(common_dict)	
