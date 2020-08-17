# -*- coding: utf-8 -*-
"""
Created on 25/06
13 - File cycle, read csv, compute Force, save vtk with same name, Without pd
14 - New Scalar variables: Force, Strain
@author: MM42910
"""

import numpy as np
import struct as st
import csv
import os, sys, time

### 0 Prelude
# Argument read - inline
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
    if caseName in name and 'csv' in name and 'stats' not in name]

tic = time.perf_counter()

### 1 loop
for name in CsvList:
    ### 11 Read csv
    tic_loop = time.perf_counter()
    currentCaseName = folder+"/"+name
    
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
    fic = open(folder+"/"+name[:-4]+".vtk", "wb")
        
    fic.write(b'# vtk DataFile Version 3.0\n')
    fic.write(b'Generate VTK output from RootSPH for Paraview read\n')
    fic.write(b'BINARY\n')
    fic.write(b'DATASET POLYDATA\n')
    fic.write(b'POINTS '+bytes(str(N), 'utf-8')+b' float\n')
    for row in dP:
        fic.write(st.pack(">f", float(row['Pos.x']))
         +st.pack(">f", float(row['Pos.y']))
         +st.pack(">f", float(row['Pos.z'])))
    fic.write(b'\n')
        
    fic.write(b'VERTICES '+bytes(str(N), 'utf-8')
     +b' '+bytes(str(2*N), 'utf-8')+b'\n')
    
    i = 0
    for row in dP:
        fic.write(st.pack(">i", 1)+st.pack(">i", i))
        i += 1
    fic.write(b'\n')    
    
    fic.write(b'POINT_DATA '+bytes(str(N), 'utf-8')+b'\n')
    fic.write(b'SCALARS Idp unsigned_int\n')
    fic.write(b'LOOKUP_TABLE default\n')
    for row in dP:
        fic.write(st.pack(">i", int(row['Idp'])))
    fic.write(b'\n')
        
    # Field variables    
    fic.write(b'FIELD FieldData '
     +bytes(str(len(dP_sca)+len(dP_vec)+7), 'utf-8')+b'\n')
    
    # Scalar loop
    for item in dP_sca:
        fic.write(bytes(item, 'utf-8')+b' 1 '+bytes(str(N), 'utf-8')+b' float\n')
        for row in dP:
            fic.write(st.pack(">f", float(row[item])))
        fic.write(b'\n')     
    
    # Vector loop
    for item in dP_vec:
        fic.write(bytes(item, 'utf-8')+b' 3 '+bytes(str(N), 'utf-8')+b' float\n')
        for row in dP:
            fic.write(st.pack(">f", float(row[item+".x"]))
            +st.pack(">f", float(row[item+".y"]))
            +st.pack(">f", float(row[item+".z"])))
        fic.write(b'\n')     
    
    # Inclusion Force
    fic.write(b'Force 3 '+bytes(str(N), 'utf-8')+b' float\n')    
    
    for row in dForce:
        fic.write(st.pack(">f", row['Force.x'])
        +st.pack(">f", row['Force.y'])
        +st.pack(">f", row['Force.z'])) 
    fic.write(b'\n')    
    
    # Inclusion Magnitude Force
    fic.write(b'Force_Mg 1 '+bytes(str(N), 'utf-8')+b' float\n')
    for row in dForce:
        fic.write(st.pack(">f", np.sqrt(
                row['Force.x']**2+row['Force.y']**2+row['Force.z']**2)))
    fic.write(b'\n')   
    
    fic.write(b'ForceVisc_Mg 1 '+bytes(str(N), 'utf-8')+b' float\n')
    for row in dP:
        fic.write(st.pack(">f", np.sqrt(
            (float(row['AceVisc.x'])*float(row['Mass']))**2
            +(float(row['AceVisc.y'])*float(row['Mass']))**2
            +(float(row['AceVisc.z'])*float(row['Mass']))**2)))
    fic.write(b'\n') 
    
    fic.write(b'AceVisc_Mg 1 '+bytes(str(N), 'utf-8')+b' float\n')
    for row in dP:
        fic.write(st.pack(">f", np.sqrt(
            float(row['AceVisc.x'])**2
            +float(row['AceVisc.y'])**2
            +float(row['AceVisc.z'])**2)))
    fic.write(b'\n') 
    
    # Inclusion Magnitude Strain
    fic.write(b'Strain_Mg 1 '+bytes(str(N), 'utf-8')+b' float\n')
    for row in dP:
        fic.write(st.pack(">f", np.sqrt(float(row['StrainDot.x'])**2
         +float(row['StrainDot.y'])**2+float(row['StrainDot.z'])**2)))
    fic.write(b'\n')  
    
    # Inclusion Radial velocity Y+Z
    fic.write(b'RadVel_YZ 3 '+bytes(str(N), 'utf-8')+b' float\n')
    for row in dP:
        fic.write(st.pack(">f", 0)
        +st.pack(">f", float(row['Vel.y']))
        +st.pack(">f", float(row['Vel.z']))) 
    fic.write(b'\n')  
    
    fic.write(b'RadVel_YZ_Mg 1 '+bytes(str(N), 'utf-8')+b' float\n')
    for row in dP:
        fic.write(st.pack(">f", np.sqrt(float(row['Vel.y'])**2
                      +float(row['Vel.z'])**2)))
    fic.write(b'\n')  
    
    # Tensor loop
    fic.write(b'TENSORS Ellipsoids float\n')
    for row in dTen:
        M = np.matrix([[row['Qf.xx'], row['Qf.xy'], row['Qf.xz']]
        ,[row['Qf.xy'], row['Qf.yy'], row['Qf.yz']]
        ,[row['Qf.xz'], row['Qf.yz'], row['Qf.zz']]])
        E, R = np.linalg.eig(M)
        EM = np.matrix([[1/E[0]**0.5, 0, 0],[0, 1/E[1]**0.5, 0],[0, 0, 1/E[2]**0.5]])
        TM = np.matmul(R, np.matmul(EM,R.transpose()))
        fic.write(st.pack(">f", TM[0,0])+st.pack(">f", TM[0,1])
         +st.pack(">f", TM[0,2])+st.pack(">f", TM[1,0])+st.pack(">f", TM[1,1])
         +st.pack(">f", TM[1,2])+st.pack(">f", TM[2,0])+st.pack(">f", TM[2,1])
         +st.pack(">f", TM[2,2]))      
    fic.write(b'\n')  
    fic.close()
    toc_loop = time.perf_counter()
    print(name[:-4]+f" complete: {toc_loop - tic_loop:0.4f} s")

toc = time.perf_counter()
print(caseName+f" complete: {toc - tic:0.4f} s")
