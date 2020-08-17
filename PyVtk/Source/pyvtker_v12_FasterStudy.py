# -*- coding: utf-8 -*-
"""
Created on Thu May 14 13:42:20 2020
File cycle, read csv, compute Force, save vtk with same name
All parameters included scalar, vectors, tensors

@author: MM42910
"""

import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
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
    dfP_vec = [item[:-2] for item in dfP.columns.values.tolist() if '.x' in item 
               and 'Pos' not in item]
    dfP_ten = [item[:-2] for item in dfP.columns.values.tolist() if 'xx' in item]
    dfP_sca = [item for item in dfP.columns.values.tolist() if '.' not in item 
               and 'Qf' not in item and ': ' not in item]
    
    ### 2 Compute Force
    dfForce = pd.concat([dfP['Acec.x']*dfP['Mass'], dfP['Acec.y']*dfP['Mass']
         , dfP['Acec.z']*dfP['Mass']], axis=1
         , keys=['Force.x', 'Force.y', 'Force.z'])
    
    ### 2b Compute Ellipsoids
    dfTensors = pd.concat([dfP['Qfxx'], dfP['Qfyy'], dfP['Qfzz']
         , dfP['Qfxy'], dfP['Qfxz'], dfP['Qfyz']], axis=1
         , keys=['Qf.xx', 'Qf.yy', 'Qf.zz', 'Qf.xy', 'Qf.xz', 'Qf.yz'])
    #// TO BE DONE //#
#    for row in dfTensors.itertuples():
#        M = np.matrix([[row._1, row._4, row._5],[row._4, row._2, row._6],[row._5, row._6, row._3]])
#        E, R = np.linalg.eig(M)
#        EM = np.matrix([[1/E[0]**0.5, 0, 0],[0, 1/E[1]**0.5, 0],[0, 0, 1/E[2]**0.5]])
#        TM = np.matmul(R, np.matmul(EM,R.transpose()))
#        
#    dfEllipsoids = dfTensors
#    eigenValues, passMatrix = numpy.linalg.eig(matOrg);
#    newDiag = numpy.zeros((3, 3))
#    i = 0
#    for val in eigenValues :
#        newDiag[i][i] = 1./math.sqrt(val)
#        i += 1
#    return numpy.matmul(passMatrix, numpy.matmul(newDiag, passMatrix.transpose()))

    ### 3 Write down the VTK
    # Create file and write in it
    N = len(dfP)
    fic = open("..\\Output\\All_"+name[:-4]+".vtk", "w")
    
    fic.write("# vtk DataFile Version 3.0\nTest VTK file for Force data\n"+
            "ASCII\nDATASET POLYDATA\nPOINTS {} float\n".format(N))
    
#    dicP = dfP.set_index('Idp').T.to_dict('list')
    dicP = dfP.T.to_dict('dict')
    tic = time.perf_counter()
    
    for index in dicP :
        fic.write("{} {} {}\n".format(dicP[index]["Pos.x"], dicP[index]["Pos.y"], dicP[index]["Pos.z"]))
            
    fic.write("VERTICES {} {}\n".format(N, N*2))
    i = 0    
    for index in dicP :
        fic.write("1 {}\n".format(index))
        
    fic.write("POINT_DATA {}\nSCALARS Idp unsigned_int\nLOOKUP_TABLE default\n".format(N))
    for index in dicP :
        fic.write("{} ".format(int(dicP[index]["Idp"])))
    fic.write("\n")
    
    # Field variables    
    dataField = "FIELD FieldData {}\n".format(len(dfP_sca)+len(dfP_vec)+1)
    
    # Scalar loop
    for item in dfP_sca:
        dataField += "{} {} {} {}\n".format(item, 1, N, "float")
        for index in dicP:
            fic.write("{} ".format(dicP[index][item])) 
        fic.write("\n")               
    
    # Vector loop
    for item in dfP_vec:
        dataField += "{} {} {} {}\n".format(item, 3, N, "float")
        for index in dicP:
            fic.write("{} {} {} ".format(dicP[index][item+".x"]
            , dicP[index][item+".y"], dicP[index][item+".y"]))
        fic.write("\n")               
        
    
    # Inclusion Force
    dataField += "{} {} {} {}\n".format("Force", 3, N, "float")
    for row in dfForce.itertuples():
        dataField += "{} {} {} ".format(row._1, row._2, row._3) 
    dataField += "\n"
    
    # Tensor loop
    dataField += "{} {} {}\n".format("TENSORS", "Ellispoids", "float")
    for index in dicP :
        fic.write("{} {} {}\n".format(dicP[index]["Pos.x"], dicP[index]["Pos.y"], dicP[index]["Pos.z"]))
        M = np.matrix(
                [[dicP[index]["Qfxx"], dicP[index]["Qfxy"], dicP[index]["Qfxz"]]
                ,[dicP[index]["Qfxy"], dicP[index]["Qfyy"], dicP[index]["Qfyz"]]
                ,[dicP[index]["Qfxz"], dicP[index]["Qfyz"], dicP[index]["Qfzz"]]])
        E, R = np.linalg.eig(M)
        EM = np.matrix([[1/E[0]**0.5, 0, 0],[0, 1/E[1]**0.5, 0],[0, 0, 1/E[2]**0.5]])
        TM = np.matmul(R, np.matmul(EM,R.transpose()))
        fic.write("{} {} {} {} {} {} {} {} {} ".format(
            TM[0,0], TM[0,1], TM[0,2], TM[1,0], TM[1,1]
            , TM[1,2], TM[2,0], TM[2,1], TM[2,2]))
         
    fic.write("\n")
    
    fic.write(dataField)  
    toc = time.perf_counter()
    print(name+f" complete: {toc - tic:0.4f} s")
    fic.close()
