# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 19:54:02 2017

@author: kyleh
"""

import DataLoad as dl
import A_Priori as AP

minsups=[.15,.3,.15,.3,.025,.025,.0625,.0625]
minconfs=[.5, .5, .8, .8, .5, .8, .5, .8]

rules=[]

categories=dl.get_categories()
records=dl.get_records(categories)

for i in range(8):
    ap=AP.APriori(minsups[i], minconfs[i])
    ap.generate_frequent_itemsets(records, categories)
    ap.generate_rules(records)
    for rule in ap.rules:
        if rule not in rules:
            rules.append(rule)
            
rules=sorted(rules, key=lambda x:x[4], reverse=True)
ap=AP.APriori(0,0)
ap.rules=rules
ap.print_rules(15)