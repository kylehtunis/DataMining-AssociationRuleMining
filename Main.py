# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 00:16:45 2017

@author: kyleh
"""

import DataLoad as dl
import A_Priori as AP
from collections import Counter
import time


###start timing
start=time.time()

###load data and categories
categories=dl.get_categories()
records=dl.get_records(categories)

###generate frequent itemsets
ap = AP.APriori(.3, .5)
ap.generate_frequent_itemsets(records, categories)
kCounts=Counter()
for fis in ap.frequentItemsets:
    kCounts[len(fis)]+=1
print('Frequent itemsets per K:',dict(kCounts),'\n')
#print(ap.frequentItemsets,'\n')
#print([ap.get_frequency(set(s), records) for s in ap.frequentItemsets])

###generate rules
ap.generate_rules(records)
ap.rules=sorted(ap.rules, key=lambda x:x[4],reverse=True)
ap.print_rules(5)

print('\nGenerated',len(ap.rules),'rules\n')

###finish timing
stop=time.time()
print('Runtime:',stop-start)