# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 15:21:56 2020

@author: MM42910
"""
import os, struct

### 0 Prelude
# Casename and parameters - local
caseShort = "A2"

# Directory generation - local
if not os.path.exists("..\\Output"):
    os.mkdir("..\\Output")
   
# Wild card test
listOfFiles = os.listdir('..\\Resources\\')
for entry in listOfFiles:
    if "Original" in entry and caseShort in entry:
    #print (entry[:-10])
            caseName = entry[:-9]
            
# Generate VtkFile
VtkFile = [name for name in listOfFiles 
    if caseName in name and 'stats' not in name][0]

### Read file
with open("..\\Resources\\"+VtkFile, mode='rb') as file: # b is important -> binary
    next(file)
    next(file)
    next(file)
    next(file)
    next(file)
    pointsHdle = file.read(8925*4)
    next(file)
    next(file)
    vertHdle = file.read(5950*4)
    next(file)
    next(file)
    next(file)
    next(file)
    lookHdle = file.read(2975*4)
    next(file)
    next(file)
    next(file)
    velHdle = file.read(2975*3*4)
    next(file)
    next(file)
    rhoHdle = file.read(2975*4)
    
    
print('Vel')
print(struct.unpack(">f", velHdle[:4]))
print(struct.unpack(">f", velHdle[-4:]))
print('Rhop')
print(struct.unpack(">f", rhoHdle[:4]))
print(struct.unpack(">f", rhoHdle[424:428]))
print(struct.unpack(">f", rhoHdle[-4:]))