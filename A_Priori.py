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
        fis=[]
        self.minsup*=len(records)
        candidates1=sorted(list(categories))
        for c in sorted(list(categories)):
            count=sum(1 for r in records if c in r)
#            print(c, count)
            if count<self.minsup:
                candidates1.pop(candidates1.index(c))
#        print(candidates1)
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
            for c in candidates:
                fis.append(c)
            prev=candidates.copy()
            candidates=[]
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
                    elif not self.check_subset_frequency(set(candidate), records):
                        continue
                    
                    candidates.append(candidate)
#                    print(candidates)
                else:
                    i+=1
#                print()
#            print(candidates)
#            print(len(candidates))
           
#        print(fis)
        self.frequentItemsets=fis
    
    def generate_rules(self, records):
        self.rules=[]
        for itemset in self.frequentItemsets:
            itemsetRules = self.generate_rule(itemset, records)
            for rule in itemsetRules:
                self.rules.append(rule)
        
    def generate_rule(self, fis, records):
        ruleCandidates=[]
        #generate rules with consequent size 1
        itemset=set(fis)
#        print(itemset)
        rules=[]
        for item in itemset:
            rule=(itemset-set([item]), set([item]))
#            print(rule)
            conf=self.get_confidence(rule, records)
            lift=self.get_lift(rule, records)
            if conf>=self.minconf and lift>=1:
                interestingness=len(rule[1])**2+len(rule[0])+conf*lift
                rule=(rule[0], rule[1], conf, lift, interestingness)
                ruleCandidates.append(rule)
                rules.append(rule)
        currentRule=None
        while len(ruleCandidates)>0:
            if len(ruleCandidates[0][0])==1:
                break
#            print('Current Rule:',currentRule)
            prev=ruleCandidates.copy()
#            print(prev)
            ruleCandidates=[]
            for currentRule in prev:
                for item in currentRule[0]:
                    rule=(currentRule[0]-set([item]), currentRule[1]|set([item]))
                    conf=self.get_confidence(rule, records)
                    lift=self.get_lift(rule, records)
                    if conf>=self.minconf and lift>=1:
                        interestingness=len(rule[1])**2+len(rule[0])+conf*lift
                        rule=(rule[0],rule[1],conf,lift,interestingness)
                        ruleCandidates.append(rule)
                        rules.append(rule)
#            print(ruleCandidates)
            
#        print('Returned Rule:',currentRule)
        return rules
    
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
    
    def check_subset_frequency(self, itemset, records):
        for subset in itertools.combinations(itemset, len(itemset)-1):
#            print(set(subset))
#            print(prev)
            if not self.check_if_frequent(set(subset), records):
#                print('false')
                return False
#        print('true')
        return True
    
    def get_frequency(self, itemset, records):
        count=0
        for r in records:
            if len(itemset & r)==len(itemset):
                count+=1
        return count
    
    def get_lift(self, rule, records):
        return self.get_support(rule[0]|rule[1], records)/(self.get_support(rule[0], records)*self.get_support(rule[1], records))
                                  
    def get_support(self, itemset, records):
        return self.get_frequency(itemset, records)/len(records)
    
    def print_rules(self, top=-1):
        if top==-1:
            top=len(self.rules)
        for rule in self.rules[:top]:
            print(str(rule[0])+' -> '+str(rule[1]))
            print('Confidence:',rule[2])
            print('Lift:',rule[3])
            print('Interestingness:',rule[4])