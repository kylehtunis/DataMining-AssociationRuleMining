# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 00:16:45 2017

@author: kyleh
"""

import DataLoad as dl


categories=dl.get_categories()
#print(categories)

records=dl.get_records(categories)