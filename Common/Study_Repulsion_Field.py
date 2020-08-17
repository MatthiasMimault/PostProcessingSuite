# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 15:15:29 2020
Study of a repulsion field in longitudinal direction
@author: MM42910
"""

import numpy as np
import matplotlib.pyplot as plt

### -1. Functions
def f(x,C):
    xb = 2.5
    return -C/abs(x-xb)**3
def f2(x,C):
    xb = 2.5
    return -C/abs(x-xb-0.1)**3


### 0. Inputs
C = 0.005

### 1. Variables
xx = np.arange(2.2,2.5,0.01)

### 2. Plots
#plt.plot(xx, f(xx,0.1),xx, f(xx,0.01), xx, f(xx,0.001))
plt.plot(xx, f(xx,C),xx, f2(xx,C))
#plt.xlim([0, 0.9])
plt.ylim([-5,0])
plt.ylabel('Repulsion field value')
plt.xlabel('Distance  along the root')
plt.show()
#print(dt(L,a))
