# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 23:39:32 2017

@author: kyleh
"""

import itertools


class APriori:
    
    def __init__(self, minsup, minconf):
        self.minsup=minsup
        self.minconf=minconf
        
    def generate_frequent_itemsets(self, records, categories):
        candidates1=sorted(list(categories))
        for c in sorted(list(categories)):
            count=sum(1 for r in records if c in r)
#            print(c, count)
            if count<self.minsup:
                candidates1.pop(candidates1.index(c))
        candidates=[]
        for i,c in enumerate(candidates1):
            for c2 in candidates1[i:]:
                if c==c2:
                    continue
                candidates.append([c, c2])
                count=sum(1 for r in records if c in r and c2 in r)
#                print(candidates[-1],count)
                if count<self.minsup:
                    candidates.pop()
#        print(candidates)
        print()
        prev=[]
        while len(candidates)!=0:
            prev=candidates.copy()
            candidates=[]
#            print(prev)
#            for i,c in enumerate(prev):
#                if i==0:
#                    continue
#                if prev[i-1][:-1]==c[:-1]:
#                    print(prev[i-1])
#                    print(c)
#                    candidates.append(prev[i-1])
#                    candidates[-1].append(c[-1])
#                    if not self.check_if_frequent(set(candidates[-1]), records):
#                        candidates.pop()
#                    elif not self.check_subset_frequency(set(candidates[-1]), records):
#                        candidates.pop()
#                    print(candidates)
#                    print()
            i=0
            while i != len(prev)-1:
#                print(prev[i])
#                print(prev[i+1])
                if prev[i][:-1] == prev[i+1][:-1]:
                    candidate=prev[i].copy()
                    candidate.append(prev[i+1][-1])
                    prev.pop(i+1)
                    
                    if not self.check_if_frequent(set(candidate), records):
                        continue
                    elif not self.check_subset_frequency:
                        continue
                    
                    candidates.append(candidate)
#                    print(candidates)
                else:
                    i+=1
#                print()
#            print(candidates)
#            print(len(candidates))
            
        self.frequentItemsets=prev

    def check_if_frequent(self, itemset, records):
        count=0
        for r in records:
            if len(itemset & r)==len(itemset):
                count+=1
#        print(count)
        return count>=self.minsup
    
    def check_subset_frequency(self, itemset, records):
        for subset in sorted(list(itertools.combinations(itemset, len(itemset)-1))):
            if subset not in prev:
                return False
        return True
    
    def get_frequency(self, itemset, records):
        count=0
        for r in records:
            if len(itemset & r)==len(itemset):
                count+=1
        return count