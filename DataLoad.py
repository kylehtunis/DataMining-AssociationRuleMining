# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 00:15:52 2017

@author: kyleh
"""

def get_categories():
    with open('products') as f:
        cats=f.read().splitlines()
    f.close()
    return cats

def get_records(categories):
    with open('small_basket.dat') as f:
        data=f.read().splitlines()
        records=[]
        for r in data:
            r=r.split(', ')
            r.pop(0)
            record=set()
            for i, item in enumerate(r):
                if item!='0':
                    record.add(categories[i])
            records.append(record)
    f.close()
    return records