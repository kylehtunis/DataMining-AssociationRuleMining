# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 23:39:32 2017

@author: kyleh
"""

import itertools
from scipy import optimize


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
                    elif not self.check_subset_frequency(set(candidate), prev, records):
                        continue
                    
                    candidates.append(candidate)
#                    print(candidates)
                else:
                    i+=1
#                print()
#            print(candidates)
#            print(len(candidates))
            
        self.frequentItemsets=prev
    
    def generate_rules(self, records):
        self.rules=[]
        for itemset in self.frequentItemsets:
            rule = self.generate_rule(itemset, records)
            if rule is not None:
                self.rules.append(rule)
        
    def generate_rule(self, fis, records):
        ruleCandidates=[]
        #generate rules with consequent size 1
        itemset=set(fis)
#        print(itemset)
        for item in itemset:
            rule=(itemset-set([item]), set([item]))
#            print(rule)
            conf=self.get_confidence(rule, records)
            if conf >= self.minconf:
                ruleCandidates.append(rule)
        currentRule=None
        while len(ruleCandidates)>0:
            bestRule=None
            bestConf=0
            for rule in ruleCandidates:
                conf=self.get_confidence(rule, records)
                if conf>bestConf:
                    bestConf=conf
                    bestRule=rule
#            print('Best Rule:',bestRule)
            currentRule=bestRule
            if len(bestRule[0])==1:
                break
#            print('Current Rule:',currentRule)
            ruleCandidates=[]
            for item in currentRule[0]:
                rule=(currentRule[0]-set([item]), currentRule[1]|set([item]))
                if self.get_confidence(rule, records) >= self.minconf:
                    ruleCandidates.append(rule)
#            print(ruleCandidates)
            
#        print('Returned Rule:',currentRule)
        return currentRule
    
    def get_confidence(self, rule, records):
        antecedentCount=0
        correctCount=0
        for r in records:
            rs=set(r)
            if len(rule[0]&rs) == len(rule[0]):
                antecedentCount+=1
                if len(rule[1]&rs) == len(rule[1]):
                    correctCount+=1
        return correctCount/antecedentCount

    def check_if_frequent(self, itemset, records):
        count=0
        for r in records:
            if len(itemset & r)==len(itemset):
                count+=1
#        print(count)
        return count>=self.minsup
    
    def check_subset_frequency(self, itemset, prev, records):
        for subset in sorted(list(itertools.combinations(itemset, len(itemset)-1))):
            print(list(subset))
            print(prev)
            if subset not in prev:
                print('false')
                return False
        print('true')
        return True
    
    def get_frequency(self, itemset, records):
        count=0
        for r in records:
            if len(itemset & r)==len(itemset):
                count+=1
        return count
    
    def print_rules(self):
        for rule in self.rules:
            print(str(rule[0])+' -> '+str(rule[1]))