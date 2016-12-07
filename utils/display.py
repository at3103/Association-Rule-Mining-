import operator
import re

# Function to print and save to output file the Frequent Item Set and High-confidence Association Rules
def display(L_k, length, minimum, flag):
	
	header = {0: "\n==Frequent Item Sets==(min_sup="+ str(minimum*100) + "%)==\n" ,
			  1: "\n==High-confidence association rules==(min_conf = "+
			  str(minimum*100) + "%)==\n"}

	file_mode = {0:'w',
				 1:'a'}
	common_dict = {}

	if flag == 0:
		for itemset in L_k:
			common_dict.update(itemset)
	else:
		for rules in L_k:
			index = "[" + rules[0][0] + "] => [" + rules[0][1] + "]"
			itemset = {index:[rules[1],rules[2]]}
			common_dict.update(itemset)

	# Sorting the frequent Itemsets based on decreasing order of support/Sorting the Rules based on decreasing order of confidence			
	common_dict = sorted(common_dict.items(), key=operator.itemgetter(1,0), reverse=True)
	
	with open ('output.txt', file_mode[flag]) as file:
		print_string = header[flag]
		print print_string
		file.write(print_string)
		for i in common_dict:
			temp = i[0].replace('&&',', ').replace('"','')
			if flag:
				i = tuple([re.sub('\d+_','',temp), [float(i[1][0]*100.0), float(i[1][1]*100.0/length)]]) 
				print_string = i[0] + ", Conf: "+str(i[1][0])+"%, Supp: "+str(i[1][1]) + "%\n"
			else:
				i =tuple([re.sub('\d+_','',temp), float(i[1]*100.0/length)]) 
				print_string = "[" + i[0] + "], "+str(i[1]) + "%\n"

			print print_string.strip()
			file.write(print_string)

	return

