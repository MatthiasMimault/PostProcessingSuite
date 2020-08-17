# -*- coding: utf-8 -*-
"""
Created on Thu May 14 13:42:20 2020
File cycle, read csv, compute Force, save vtk with same name

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
            #print (entry[:-10])
            caseName = entry[:-10]
            
# Generate list of Csv names
CsvList = [name for name in listOfFiles 
    if caseName in name and 'stats' not in name]

### 1 loop
for name in CsvList:
    ### 11 Read csv
    currentCaseName = "..\\Csv\\"+name
    dfP = pd.read_csv(currentCaseName,sep = ";", header=2)
            
    ### 2 Compute Force
    dfHandle = pd.concat([dfP['Pos.x'], dfP['Pos.y'], dfP['Pos.z']], axis=1
         , keys=['Pos.x', 'Pos.y', 'Pos.z'])
    dfHandle.insert(3,'Force.x',dfP['Acec.x']*dfP['Mass'],True)
    dfHandle.insert(4,'Force.y',dfP['Acec.y']*dfP['Mass'],True)
    dfHandle.insert(5,'Force.z',dfP['Acec.z']*dfP['Mass'],True)
    tic = time.perf_counter()

    ### 3 Write down the VTK
    # Create file and write in it
    N = len(dfHandle)
    NF = len(dfHandle.columns)
    fic = open("..\\Output\\"+name[:-4]+".vtk", "w")
    
    fic.write("# vtk DataFile Version 3.0\nTest VTK file for Force data\n"+
            "ASCII\nDATASET POLYDATA\nPOINTS {} float\n".format(N))
    for index, row in dfP.iterrows():
        fic.write("{} {} {}\n".format(row['Pos.x'], row['Pos.y'], row['Pos.z']))
    fic.write("VERTICES {} {}\n".format(N, N*2))
    i = 0
    for index, row in dfP.iterrows():
        fic.write("1 {}\n".format(i))
        i += 1
    fic.write("POINT_DATA {}\nSCALARS Idp unsigned_int\nLOOKUP_TABLE default\n".format(N))
    for index, row in dfP.iterrows():
        fic.write("{} ".format(int(row["Idp"])))
    fic.write("\n")
    # Field variables
    fic.write("FIELD FieldData {}\n{} {} {} {}\n".format(1,"Force", 3, N, "float"))
    for index, row in dfHandle.iterrows():
        fic.write("{} {} {} ".format(row["Force.x"], row["Force.y"], row["Force.z"]))
    fic.write("\n")
    fic.close()
    toc = time.perf_counter()
    print(name+f" complete: {toc - tic:0.4f} s")
