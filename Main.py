# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 00:16:45 2017

@author: kyleh
"""

import DataLoad as dl
import A_Priori as AP


###load data and categories
categories=dl.get_categories()
records=dl.get_records(categories)

###generate frequent itemsets
ap = AP.APriori(.02, .5)
ap.generate_frequent_itemsets(records, categories)
#print(ap.frequentItemsets,'\n')
#print([ap.get_frequency(set(s), records) for s in ap.frequentItemsets])

###generate rules
ap.generate_rules(records)
ap.rules=sorted(ap.rules, key=lambda x:x[2]*x[3])
ap.print_rules()