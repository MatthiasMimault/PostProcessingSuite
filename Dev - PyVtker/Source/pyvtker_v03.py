# -*- coding: utf-8 -*-
"""
Created on Thu May 14 13:42:20 2020
one file, read csv, compute Force, save vtk with same name
Writing time improvement
@author: MM42910
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os, fnmatch
import time

### 0 Prelude
# Casename and parameters
caseShort = "A2"

# Directory generation
if not os.path.exists("..\\Output"):
    os.mkdir("..\\Output")
   
# Wild card test
listOfFiles = os.listdir('..\\Csv\\')
for entry in listOfFiles:
    if fnmatch.fnmatch(entry, "*_stats.csv") and fnmatch.fnmatch(entry, caseShort+"*"):
            print (entry[:-10])
            caseName = entry[:-10]

### 1 Read csv
currentCaseName = "..\\Csv\\"+caseName+"_0010.csv"
dfP = pd.read_csv(currentCaseName,sep = ";", header=2)
            
### 2 Compute Force
dfHandle = pd.concat([dfP['Pos.x'], dfP['Pos.y'], dfP['Pos.z']], axis=1
                     , keys=['Pos.x', 'Pos.y', 'Pos.z'])
dfHandle.insert(3,'Force.x',dfP['Acec.x']*dfP['Mass'],True)
dfHandle.insert(4,'Force.y',dfP['Acec.y']*dfP['Mass'],True)
dfHandle.insert(5,'Force.z',dfP['Acec.z']*dfP['Mass'],True)

### 3 Write down the VTK
# Create file and write in it
tic = time.perf_counter()
N = len(dfHandle)
NF = len(dfHandle.columns)
fic = open("..\\Output\\"+caseName+"_TimeTest.vtk", "w")
fic.write("# vtk DataFile Version 3.0\n")
fic.write("Test VTK file for Force data\n")
fic.write("ASCII\n")
fic.write("DATASET POLYDATA\n")
#fic.write("\n".join(listOfFiles))
fic.write("POINTS {} float\n".format(N))
data = ""
for index, row in dfP.iterrows():
    data += "{} {} {}\n".format(row['Pos.x'], row['Pos.y'], row['Pos.z'])
    #fic.write("{} {} {}\n".format(row['Pos.x'], row['Pos.y'], row['Pos.z']))
#print(data)
fic.write(data)
fic.write("VERTICES {} {}\n".format(N, N*2))
i = 0
dataVertices = ""
for index, row in dfP.iterrows():
    data += "1 {}\n".format(i)
    i += 1
fic.write(dataVertices)
fic.write("POINT_DATA {}\n".format(N))
fic.write("SCALARS Idp unsigned_int\n")
fic.write("LOOKUP_TABLE default\n")
dataLookup = ""
for index, row in dfP.iterrows():
    dataLookup += "{} ".format(int(row["Idp"]))
fic.write(dataLookup+"\n")
# Field variables
fic.write("FIELD FieldData {}\n".format(1))
fic.write("{} {} {} {}\n".format("Force", 3, N, "float"))
dataForce = ""
for index, row in dfHandle.iterrows():
    dataForce += "{} {} {} ".format(row["Force.x"], row["Force.y"], row["Force.z"])
fic.write(dataForce+"\n")
fic.close() 
toc = time.perf_counter()
print(caseName+f" complete: {toc - tic:0.4f} s")