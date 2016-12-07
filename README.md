# Association-Rule-Mining

TEAM 9
Ashwin Tamilselvan (at3103)
Niharika Purbey (np2544)

******* TO DO *********
Document Structure:
```
main.py:
output.txt:
example-run.txt:

algorithms - 
	apriori.py:
Data_Set_gen -
	Data_prepare.py:
	pre_vectorzing.py:
	vectorizing.py:
	CSV files - 
		INTEGRATED-DATASET.csv
utils - 
	display.py
```


a) We used the 3-1-1 Call Center Inquiry dataset from the NYC Open Data set to generate the INTEGRATED-DATASET file (https://data.cityofnewyork.us/view/tdd6-3ysr)

b) The original dataset contains 58,435,089 rows with information about call inquiries from 2010 - present day. Since the dataset was huge, we decided to work on the data for Jan 2015 and Feb 2015 only. 

The original dataset had the columns: Unique Key, Date, Time, Agency, Inquiry Name, Brief Description, Call Resolution. We deleted the column "Brief Description" because the descriptions were similar to "inquiry name", hence redundant. 

To get interesting rules, we decided to focus on the top 5 agencies (i.e. top 5 agencies with maximum number of tuples). The top 5 agencies were DOF, NYPD, 3-1-1, DSNY, HPD. 

This initial filtering was done on the website itself. 

After downloading this data, we had around 500,000 rows, so we decided to use a stratified sample of this data. We performed stratified sampling based on the column "call resolution" to get a uniform distribution on the values of "call resolution". We used the Python library 'sklearn' to do this. Script can be found in Data_Set_gen/Data_prepare.py     

To further generate interesting results, we converted the date to day of the week and converted the raw time to designated time-zones i.e "Morning","Noon","Evening" and "Night" where "Morning":6am-12pm ; "Noon":12pm-6pm ; "Evening":6pm-12am ; "Night":12am-6am. The script to perform this operation can be found in Data_Set_gen/pre_vectorizing.py     

c) ******* TO DO ********* what makes your choice of INTEGRATED-DATASET file interesting (in other words, justify your choice of NYC Open Data data set(s))

We were interested in finding out what the call resolutions were for different types of inquiry. Also, we wanted to know if there is a specific day of the week or a specific time when people made more inquiries or people made more of a particular type of inquiry. 
It would also be interesting to know if certain call resolutions were linked to certain time of the day or day of the week. Or if the agencies were linked to any particular call resolution or type of inquiry.

Since there is a lot of data on this on the NYC Dataset, it would be difficult to visualize interesting patterns by simply viewing it in charts. Hence, we require association rules to find interesting relationships between the different atrributes of the dataset. 

[DOF, Noon] => [Information Provided], Conf: 47.1957671958%, Supp: 3.969949441%
[Evening, DOF] => [Information Provided], Conf: 47.1355311355%, Supp: 5.72705262408%


d) To run :
```
python main.py Integrated_data_set.csv <min_sup> <min_conf>
where min_sup = Minimum support (value between 0 and 1)
min_conf = Minimum confidence (value between 0 and 1)

Example run: python main.py Integrated_data_set.csv 0.01 0.04
```

e) Internal Design
1. For ease of use, we started by vectorizing the dataset. The script in Data_Set_gen/vectorizing.py performs this operation. We saved the vectorized data as a CSV file, wherein each value in each of the columns were now columns in this new CSV file.

2. We then ran the Apriori algorithm on the dataset. The Apriori algorithm implementation is as given in the paper "Fast algorithms for Mining Association Rules" sections 2.1 and 2.1.1.

3. We first generate L1 i.e. 1-large itemsets by simply summing values of each of the columns in the vectorized CSV file and checking whether it is greater than the minimum support. The columns in the vectorized CSV file represent all the items. 

4. We then generate the candidate itemsets(C_k) by joining L_k-1 with itself. We then prune this set by checking if the (k-1)—item subsets of this set are present in large (k-1)—itemset. Hence, after the prune method the final C_k is generated.

5. We then calculate the support for each of the items in the set C_k by simply 'anding' the corresponding columns from the vectorized dataset and summing the final result. From this, we retain all those items that have support greater than minimum support in the Large itemset (L_k).   

6. We continue this process(steps 4 and 5) until the Large itemset generated(L_k) is null.

7. We then generate rules from the Large Itemsets i.e L1, L2, L3,... (till whenever the algorithm ran to). Here we calculate the confidence of each rule as conf(LHS=>RHS) = sup(LHS U RHS)/sup(LHS). We retain only those rules whose confidence is greater than the input minimum confidence. 

8. We then print these rules in decreasing order of confidence along with the frequent itemsets in decreasing order of support. We also save this to an output file. 


f) Interesting Results
```
python main.py Integrated_data_set.csv 0.03 0.3 

[Monday] => [Evening], Conf: 44.8522118627%, Supp: 8.05027415794%
[Friday] => [Evening], Conf: 44.7794779478%, Supp: 7.08538061668%
[Wednesday] => [Evening], Conf: 44.5170840015%, Supp: 6.42490920743%
[Thursday] => [Evening], Conf: 43.4210526316%, Supp: 7.1085238197%
[Tuesday] => [Evening], Conf: 43.1402273958%, Supp: 7.09250160222%
[Saturday] => [Evening], Conf: 39.0065604499%, Supp: 3.70469272947%
[Sunday] => [Evening], Conf: 38.8628260462%, Supp: 3.68689026561%


From the above results, we can infer that the majority of the calls placed were during the evening period(6 PM
- 12 AM). As the time zones form a mutually exclusive and exhaustive set, we can derive a clean breakup of the
various time zones of the day. 

The support of the above rules conforms to the hypothesis that the number of queries would be more during the
weekdays, as not all the agencies would be working over the weekend. Only urgent calls/queries are made
during the weekend, and the support values of Saturday/Sunday in comparision to the weekends are a good
indicative of it.

```

```
For 100,000
python main.py Integrated_data_set.csv 0.03 0.3 v



```
******* TO DO - Discuss interesting results ********

