import pylab as pl


from Framework.DataSet import *
from Tools import writeapriorifile

dataset = DataSet(
	datafile ='../data/normalized.csv',
	na_values=['?'],
	string_columns=['state','communityname'],
)

dataset = dataset.drop_columns([
    'state',
    'communityname',
	'fold',
#	'murders', 'murdPerPop',
#	'rapes', 'rapesPerPop',
#	'robberies', 'robbbPerPop',
#	'assaults', 'assaultPerPop',
#	'burglaries', 'burglPerPop',
#	'larcenies', 'larcPerPop',
#	'autoTheft', 'autoTheftPerPop',
#	'arsons', 'arsonsPerPop',
#	'ViolentCrimesPerPop',
#	'nonViolPerPop',
])
#dataset = dataset.standardize()
dataset = dataset.take_columns([
    'racepctblack',
    'racePctWhite',
    'racePctAsian',
    'racePctHisp',

    'PctPopUnderPov',
    'medIncome',

    #'PctImmigRecent',
    'NumStreet',

    'ViolentCrimesPerPop',
]);
print(dataset.df['NumStreet'])
dataset = dataset.fix_missing(drop_objects=True)


#dataset = dataset.discretize('arsons', 2)

dataset = dataset.binarize()

print(dataset.X)

filename = '../tmp/apriori.txt'


writeapriorifile.WriteAprioriFile(dataset.X, filename=filename)





import numpy as np
import subprocess
from subprocess import call
import re
import os

minSup = 40
minConf = 80
maxRule = 6


# Run Apriori Algorithm
print('Mining for frequent itemsets by the Apriori algorithm')
status1 = call('apriori -f"," -s{0} {1} ../tmp/apriori_temp1.txt'.format(minSup, filename),shell=True)
if status1!=0:
    print('An error occured while calling apriori, a likely cause is that minSup was set to high such that no frequent itemsets were generated or spaces are included in the path to the apriori files.')
    exit()
if minConf>0:
    print('Mining for associations by the Apriori algorithm')
    status2 = call('apriori -tr -f"," -n{0} -c{1} -s{2} -v" (%C)" {3} ../tmp/apriori_temp2.txt'.format(maxRule, minConf, minSup, filename), shell=True)
    if status2!=0:
        print('An error occured while calling apriori')
        exit()
print('Apriori analysis done, extracting results')


# Extract information from stored files apriori_temp1.txt and apriori_temp2.txt
f = open('../tmp/apriori_temp1.txt','r')
lines = f.readlines()
f.close()
# Extract Frequent Itemsets
FrequentItemsets = ['']*len(lines)
sup = np.zeros((len(lines),1))
for i,line in enumerate(lines):
    FrequentItemsets[i] = line[0:-1]
    sup[i] = float(re.findall('\(.*\)', line)[0][1:-1])
os.remove('../tmp/apriori_temp1.txt')
    
# Read the file
f = open('../tmp/apriori_temp2.txt','r')
lines = f.readlines()
f.close()
# Extract Association rules
AssocRules = ['']*len(lines)
conf = np.zeros((len(lines),1))
for i,line in enumerate(lines):
    AssocRules[i] = line[0:-1]
    conf[i] = float(re.findall('\(.*\)', line)[0][1:-1])
os.remove('../tmp/apriori_temp2.txt')    

# sort (FrequentItemsets by support value, AssocRules by confidence value)
AssocRulesSorted = [AssocRules[item] for item in np.argsort(conf,axis=0).ravel()]
AssocRulesSorted.reverse()
FrequentItemsetsSorted = [FrequentItemsets[item] for item in np.argsort(sup,axis=0).ravel()]
FrequentItemsetsSorted.reverse()
    

fnPretty =  lambda m: dataset.df.columns[int(m.group(1))] + " "

# Print the results
import time; time.sleep(.5)    
print('\n')
print('RESULTS:\n')
print('Frequent itemsets:')
for i,item in enumerate(FrequentItemsetsSorted):
    item = re.sub(r'(\d+) ', fnPretty, item)
    print('Item: {0}'.format(item))
print('\n')
print('Association rules:')
for i,item in enumerate(AssocRulesSorted):
    item = re.sub(r'(\d+) ', fnPretty, item)
    print('Rule: {0}'.format(item))


