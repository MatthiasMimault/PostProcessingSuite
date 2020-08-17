# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 11:09:02 2020
Study to average same index values from a list of dictionaries
1 - Method 1 from Geekforgeek: Unsatisfying, remove zeros (b)

@author: MM42910
"""

import collections
#import functools, operator 

D1 = {'a':1, 'b':2, 'c':3}
D2 = {'a':5, 'b':-2, 'c':2}

#result = dict(functools.reduce(operator.add, 
#         map(collections.Counter, [D1,D2]))) 
#print(map(collections.Counter, [D1,D2]))

# sum the values with same keys 
counter = collections.Counter() 
for d in [D1,D2]:  
    d.update([0.5*d[a] for a in d.keys()])
    #counter.update([a:0.5*d[a] for a in d.keys()]) 
      
result = dict(counter) 
  
  
print("resultant dictionary : ", str(counter)) 