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

###generate rules
ap = AP.APriori(200, .5)
ap.generate_frequent_itemsets(records, categories)
print(ap.frequentItemsets)
print([ap.get_frequency(set(s), records) for s in ap.frequentItemsets])