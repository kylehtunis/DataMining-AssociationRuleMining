# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 00:16:45 2017

@author: kyleh
"""

import DataLoad as dl
import A_Priori as AP
from collections import Counter
import time
import argparse


###start timing
start=time.time()

###get minconf and minsup
parser = argparse.ArgumentParser()  
parser.add_argument('-s', '--minsup', help='set minsup', default=.25)
parser.add_argument('-c', '--minconf', help='set minconf', default=.8)
parser.add_argument('-n', '--numberOfRules', help='indicates the number of rules to print, -1 for all', default=-1)
args=parser.parse_args()
minconf=float(args.minconf)
minsup=float(args.minsup)
top=int(args.numberOfRules)
print('\nminsup:',minsup)
print('minconf:',minconf)

###load data and categories
categories=dl.get_categories()
records=dl.get_records(categories)

###generate frequent itemsets
ap = AP.APriori(minsup, minconf)
ap.generate_frequent_itemsets(records, categories)
kCounts=Counter()
for fis in ap.frequentItemsets:
    kCounts[len(fis)]+=1
print('\nFrequent itemsets per K:',dict(kCounts),'\n')
#print(ap.frequentItemsets,'\n')
#print([ap.get_frequency(set(s), records) for s in ap.frequentItemsets])

###generate rules
ap.generate_rules(records)
ap.rules=sorted(ap.rules, key=lambda x:x[4],reverse=True)
ap.print_rules(top)

print('\nGenerated',len(ap.rules),'rules\n')

###finish timing
stop=time.time()
print('Runtime:',stop-start)