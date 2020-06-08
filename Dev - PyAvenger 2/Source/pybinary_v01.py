# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 16:33:04 2020
Binary file reader
@author: MM42910
"""
import struct as s
import numpy as np

filename = '../Resources/A2-AceShortVtkOriginal_0010.vtk'

with open(filename, "rb") as f:
    next(f)
    next(f)
    next(f)
    next(f)
    
    # Points
    NP = int(str(f.readline()).split()[1])    
    for i in range(NP):
        x = s.unpack('>f', f.read(4))[0]
        y = s.unpack('>f', f.read(4))[0]
        z = s.unpack('>f', f.read(4))[0]
    next(f)
    
    # Vertices
    for i in range(NP):
        y = s.unpack('>f', f.read(4))[0]
        z = s.unpack('>f', f.read(4))[0]
    next(f)
    
    # Points data
    print(f.readline())
    
    # Scalars
    print(f.readline())
    
    # Lookup
    print(f.readline())
    for i in range(NP):
        idp = s.unpack('>i', f.read(4))[0]
    next(f)
    
    # Field
    Nfield = int(str(f.readline()).split()[2][:-3]) 
    for i in range(Nfield):
        head = str(f.readline())
        print(head)
        for j in range(NP): 
            if int(head.split()[1]) == 1:
                if head.split()[3][:-3] == 'float':    
                    d = s.unpack('>f', f.read(4))[0]
                else:
                    d = s.unpack('>s', f.read(1))[0]
                    print(d,j)
            else:
                dx = s.unpack('>f', f.read(4))[0]
                dy = s.unpack('>f', f.read(4))[0]
                dz = s.unpack('>f', f.read(4))[0]
        next(f)
    next(f)