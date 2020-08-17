# -*- coding: utf-8 -*-
"""
Created on 25/06
13 - File cycle, read csv, compute Force, save vtk with same name, Without pd
14 - New Scalar variables: Force, Strain
@author: MM42910
"""

import numpy as np
import csv
import os, time, sys

### 0 Prelude
arguments = sys.argv
name = arguments[1]
folder = arguments[2]
   
# Wild card test
listOfFiles = os.listdir(folder)
for entry in listOfFiles:
    if "stats" in entry and name in entry:
    #print (entry[:-10])
            caseName = entry[:-10]
            
# Generate list of Csv names
CsvList = [name for name in listOfFiles 
    if caseName in name and 'stats' not in name]

### 1 loop
for name in CsvList:
    ### 11 Read csv
    currentCaseName = "..\\Csv\\"+name
    
    with open(currentCaseName) as csvfile:
        next(csvfile)
        next(csvfile)
        next(csvfile)
        dP = []
        rdP = csv.DictReader(csvfile, delimiter=";")
        for row in rdP:
            del row['']
            dP.append(row)
    
    ### 12 Separate rows
    dP_vec = [item[:-2] for item in dP[0].keys() 
                if '.x' in item and 'Pos' not in item]
    dP_ten = [item[:-2] for item in dP[0].keys() if 'xx' in item]
    dP_sca = [item for item in dP[0].keys() if '.' not in item 
               and 'Qf' not in item and ': ' not in item]
    
    ### 2 Compute Force and ellipsoids
    dForce = []
    dTen = []
    for row in dP:
        dForce.append({'Force.x': float(row['Acec.x'])*float(row['Mass'])
        , 'Force.y': float(row['Acec.y'])*float(row['Mass'])
        , 'Force.z': float(row['Acec.z'])*float(row['Mass'])})
        dTen.append({'Qf.xx': float(row['Qfxx'])
        , 'Qf.yy': float(row['Qfyy'])
        , 'Qf.zz': float(row['Qfzz'])
        , 'Qf.xy': float(row['Qfxy'])
        , 'Qf.xz': float(row['Qfxz'])
        , 'Qf.yz': float(row['Qfyz'])})

    ### 3 Write down the VTK
    # Create file and write in it
    N = len(dP)
    fic = open("..\\Output\\Dic_"+name[:-4]+".vtk", "w")
    
    fic.write("# vtk DataFile Version 3.0\nTest VTK file for Force data\n"+
            "ASCII\nDATASET POLYDATA\nPOINTS {} float\n".format(N))
    
    tic = time.perf_counter()
    data = ""
    for row in dP:
        data += "{} {} {}\n".format(row['Pos.x'], row['Pos.y'], row['Pos.z']) 
#    for row in dfP.itertuples():
#        data += "{} {} {}\n".format(row._1, row._2, row._3) 
        
    fic.write(data)
        
    fic.write("VERTICES {} {}\n".format(N, N*2))
    i = 0
    for row in dP:
        fic.write("1 {}\n".format(i))
        i += 1
        
    fic.write("POINT_DATA {}\nSCALARS Idp unsigned_int\nLOOKUP_TABLE default\n".format(N))
    dataLookup = ""
    for row in dP:
        dataLookup += "{} ".format(int(row['Idp'])) 
    fic.write(dataLookup+"\n")
    
    # Field variables    
    dataField = "FIELD FieldData {}\n".format(len(dP_sca)+len(dP_vec)+1)
    
    # Scalar loop
    for item in dP_sca:
        dataField += "{} {} {} {}\n".format(item, 1, N, "float")
        for row in dP:
            dataField += "{} ".format(row[item]) 
        dataField += "\n"                
    
    # Vector loop
    for item in dP_vec:
        dataField += "{} {} {} {}\n".format(item, 3, N, "float")
        for row in dP:
            dataField += "{} {} {} ".format(row[item+".x"], row[item+".y"], row[item+".z"]) 
        dataField += "\n"
    
    # Inclusion Force
    dataField += "{} {} {} {}\n".format("Force", 3, N, "float")
    for row in dForce:
        dataField += "{} {} {} ".format(row['Force.x'], row['Force.y'], row['Force.z']) 
    dataField += "\n"
    
    # Inclusion Magnitude Force
    dataField += "{} {} {} {}\n".format("Force_Mg", 1, N, "float")
    for row in dForce:        
        dataField += "{} ".format(np.sqrt(
                row['Force.x']**2+row['Force.y']**2+row['Force.z']**2))
    dataField += "\n"
    
    # Inclusion Magnitude Strain
    dataField += "{} {} {} {}\n".format("Strain_Mg", 1, N, "float")
    for row in dP:       
        dataField += "{} ".format(np.sqrt(
                row['StrainDot.x']**2+row['StrainDot.y']**2+row['StrainDot.z']**2))
    dataField += "\n"
    
    # Tensor loop
    dataField += "{} {} {}\n".format("TENSORS", "Ellispoids", "float")
    for row in dTen:
        M = np.matrix([[row['Qf.xx'], row['Qf.xy'], row['Qf.xz']]
        ,[row['Qf.xy'], row['Qf.yy'], row['Qf.yz']]
        ,[row['Qf.xz'], row['Qf.yz'], row['Qf.zz']]])
        E, R = np.linalg.eig(M)
        EM = np.matrix([[1/E[0]**0.5, 0, 0],[0, 1/E[1]**0.5, 0],[0, 0, 1/E[2]**0.5]])
        TM = np.matmul(R, np.matmul(EM,R.transpose()))
        dataField += "{} {} {} {} {} {} {} {} {} ".format(
            TM[0,0], TM[0,1], TM[0,2], TM[1,0], TM[1,1]
            , TM[1,2], TM[2,0], TM[2,1], TM[2,2]) 
    dataField += "\n"
    
    fic.write(dataField)  
    toc = time.perf_counter()
    print(name+f" complete: {toc - tic:0.4f} s")
    fic.close()
