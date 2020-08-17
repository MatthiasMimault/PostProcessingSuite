# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 10:25:09 2020
Study script to parametrize a coefficient in division threshold distribution
@author: MM42910
"""

import numpy as np
import matplotlib.pyplot as plt

### -1. Functions
def dt(x,a):
    return (1.0 + a * (x - 0.1)**2.0)

### 0. Inputs
a = 27.0
L = 0.6

### 1. Variables
xx = np.arange(0,L,0.001)

### 2. Plots
plt.plot(xx, dt(xx,30), label = 'a = 30.0')
plt.plot(xx, dt(xx,a), label = 'a = {}'.format(a))
plt.plot(xx, dt(xx,25), label = 'a = 25.0')
plt.legend(loc = 'upper right')
plt.xlim([0, 0.9])
plt.ylim([0, 9])
plt.ylabel('Division threshold')
plt.xlabel('Distance from the tip')
plt.show()
print(dt(L,a))