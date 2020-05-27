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

    ### 3 Write down the VTK
    # Create file and write in it
    N = len(dfHandle)
    NF = len(dfHandle.columns)
    fic = open("..\\Output\\Time_"+name[:-4]+".vtk", "w")
    
    fic.write("# vtk DataFile Version 3.0\nTest VTK file for Force data\n"+
            "ASCII\nDATASET POLYDATA\nPOINTS {} float\n".format(N))
    data = ""
    for row in dfP.itertuples():
        data += "{} {} {}\n".format(row._1, row._2, row._3) 
    #for index, row in dfP.iterrows():
    #    data += "{} {} {}\n".format(row['Pos.x'], row['Pos.y'], row['Pos.z'])
    fic.write(data)
    fic.write("VERTICES {} {}\n".format(N, N*2))
    i = 0
    for row in dfP.itertuples():
        fic.write("1 {}\n".format(i))
        i += 1
    #for index, row in dfP.iterrows():
    #    fic.write("1 {}\n".format(i))
    #    i += 1
    fic.write("POINT_DATA {}\nSCALARS Idp unsigned_int\nLOOKUP_TABLE default\n".format(N))
    dataLookup = ""
    for row in dfP.itertuples():
        dataLookup += "{} ".format(int(row.Idp)) 
#    for index, row in dfP.iterrows():
#        dataLookup += "{} ".format(int(row["Idp"]))
    fic.write(dataLookup+"\n")
    
    # Field variables    
    fic.write("FIELD FieldData {}\n{} {} {} {}\n".format(1,"Force", 3, N, "float")) 
    dataForce = ""
    tic = time.perf_counter()
    for row in dfHandle.itertuples():
        dataForce += "{} {} {} ".format(row._4, row._5, row._6) 
#    for index, row in dfHandle.iterrows():
#        dataForce += "{} {} {} ".format(row["Force.x"], row["Force.y"], row["Force.z"])    
    toc = time.perf_counter()
    print(name+f" complete: {toc - tic:0.4f} s")
    fic.write(dataForce+"\n")
    fic.close()
