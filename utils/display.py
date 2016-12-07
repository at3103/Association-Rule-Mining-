import operator
import re

global verbose

def substitute(matchobj):

	Columns_dict = {'1_': 'Day is ',
					'2_': 'Time of the day is ',
					'3_': 'Agency is ',
					'4_': 'The inquiry is ',
					'5_': 'Call resolution is '
	}
	if verbose:
		return Columns_dict[matchobj.group(0)]
	return ''

# Function to print and save to output file the Frequent Item Set and High-confidence Association Rules
def display(L_k, length, minimum, flag):
	
	global verbose
	verbose = flag/2

	header = {0: "\n==Frequent Item Sets==(min_sup="+ str(minimum*100) + "%)==\n" ,
			  1: "\n==High-confidence association rules==(min_conf = "+
			  str(minimum*100) + "%)==\n",
  			  2: "\nVerbose Output\n==High-confidence association rules==(min_conf = "+
			  str(minimum*100) + "%)==\n"}

	file_mode = {0:'w',
				 1:'a'}

	file_name = {0:'output.txt',
				 1:'verbose.txt'
	}
	common_dict = {}

	if flag == 0:
		for itemset in L_k:
			common_dict.update(itemset)
	else:
		for rules in L_k:
			if verbose:
				index = rules[0][0].replace('&&',' and ')
				index += "==>" + rules[0][1]
			else:
				index = "[" + rules[0][0] + "] => [" + rules[0][1] + "]"
			itemset = {index:[rules[1],rules[2]]}
			common_dict.update(itemset)

	# Sorting the frequent Itemsets based on decreasing order of support/Sorting the Rules based on decreasing order of confidence			
	common_dict = sorted(common_dict.items(), key=operator.itemgetter(1,0), reverse=True)
	
	with open (file_name[verbose], file_mode[flag%2]) as file:
		print_string = header[flag]
		print print_string
		file.write(print_string)
		for i in common_dict:
			temp = i[0].replace('&&',', ').replace('"','')
			if flag:
				i = tuple([re.sub('\d+_',substitute,temp), [float(i[1][0]*100.0), float(i[1][1]*100.0/length)]]) 
				print_string = i[0] + ", Conf: "+str(i[1][0])+"%, Supp: "+str(i[1][1]) + "%\n"
			else:
				i =tuple([re.sub('\d+_','',temp), float(i[1]*100.0/length)]) 
				print_string = "[" + i[0] + "], "+str(i[1]) + "%\n"

			print print_string.strip()
			file.write(print_string)

	return

