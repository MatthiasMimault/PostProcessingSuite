# -*- coding: utf-8 -*-
"""
Created on 31/01/20
@author: Matthias Mimault, Augustin Leclerc
Generate .vtk files from .csv, averaging values over n files
Version 5, with average procedure
"""
import numpy as np
import decimal as dc
import time
import pandas as pd
import os
import csv
#import math
import sys

os.chdir(".")

""" I. Definition functions """
def appF(file,f) :
    file.write("{}\n".format(f))

def appF3(file,f1,f2,f3) :
    #file.write("{} {} {}\n".format(f1, f2, f3))
    file.write("{} {} {}".format(f1, f2, f3))
    
def appI(file,i) :
    file.write("{}\n".format(i))

def appI2(file,i1,i2) :
    file.write("{} {}\n".format(i1, i2))

def appT(file,t1,t2,t3,t4,t5,t6,t7,t8,t9) :
    fic.write("{} {} {}\n{} {} {}\n{} {} {}\n\n"\
              .format(t1,t2,t3,t4,t5,t6,t7,t8,t9))
    
def computeTransformedMatrix(matOrg) :
    eigenValues, passMatrix = np.linalg.eig(matOrg);
    newDiag = np.zeros((3, 3))
    i = 0
    for val in eigenValues :
        newDiag[i][i] = 1./np.sqrt(val)
        i += 1
    return np.matmul(passMatrix, np.matmul(newDiag, passMatrix.transpose()))
    


""" II. Main """
arguments = sys.argv
caseName = arguments[1]
caseFolder = arguments[2]
tic = time.perf_counter()


# Csv reading
#CsvStatA = pd.read_csv(caseFolder + "/"+caseName+"_stats.csv",sep = ";",\
#                   header=0, nrows=1)
CsvStatB = pd.read_csv(caseFolder + "/"+caseName+"_stats.csv",sep = ";",\
                       header=2);
#Np = CsvStatA['Np'][0];
Nstart = 0;
#Nfiles = 10;
Nfiles = len(CsvStatB);
Navg = 4;

for n in range(Nstart,Nstart+Nfiles):
    # Csv read            
    TempHandle = [];
    for m in range(n, n-Navg, -1):
        if(m<0): 
            Csv0 = pd.read_csv(caseFolder + "/"+caseName+"_0000.csv",\
                       sep = ";", header=2, index_col = 'Idp');
        else: 
            Csv0 = pd.read_csv(caseFolder + "/"+caseName+"_{:04d}.csv".format(m),\
                       sep = ";", header=2, index_col = 'Idp');
        TempHandle.append(Csv0);      
        
    # Duplication of missing particles
    for i in range(len(TempHandle)-1,0,-1):
        if (TempHandle[i-1].shape != TempHandle[i].shape):
            idp = list(range(TempHandle[i].shape[0], TempHandle[i-1].shape[0]))
            #print(TempHandle[i-1].loc[idp])
            for j in range(i,len(TempHandle)):
                TempHandle[j]=TempHandle[j].append(TempHandle[i-1].loc[idp])   
                
    # Data process - Duplicate positions
    for df in TempHandle:
        df['Pos.x'] = TempHandle[0]['Pos.x']
        df['Pos.y'] = TempHandle[0]['Pos.y']
        df['Pos.z'] = TempHandle[0]['Pos.z']
        #print(df['Pos.x'])
        
    # Data process - Average over Navg 
    TempData = pd.DataFrame().reindex_like(TempHandle[0]).fillna(0)
    
    for x in TempHandle:
        TempData = TempData.add(x)
    TempData = TempData.div(Navg)
    TempData['Idp'] = TempData.index
    Data = []
    for index, row in TempData.iterrows():
        Data.append(row.tolist())
    Np = TempData.shape[0]
                       
    # Generation Vtk and Header
    vtkName = caseFolder + "/" + caseName + f"_Avg{Navg}_{n:04d}.vtk"
    fic = open(vtkName, "w+")
    fic.write("# vtk DataFile Version 3.0\n")
    fic.write("vtk output\n")
    fic.write("ASCII\n")
    fic.write("DATASET POLYDATA\n")
    
    fic.write("POINTS {} float\n".format(Np))   
    for line in Data :
        fic.write("{} {} {}\n".format(line[0], line[1], line[2]))    
        
    fic.write("VERTICES {} {}\n".format(Np,2*Np)) 
    vertices = np.transpose(np.array([np.ones(Np, dtype = int),\
        np.linspace(0,Np-1,Np, dtype = int)]))
    for line in vertices :
        fic.write("{} {}\n".format(line[0], line[1]))
        
    # Write field  data
    fic.write("POINT_DATA {}\n".format(Np))    
    fic.write("SCALARS Idp unsigned_int\n")
    fic.write("LOOKUP_TABLE default\n") 
    for line in Data :
        fic.write("{} ".format(int(line[23])))
        
    fic.write("\nFIELD FieldData {}\n".format(9))
    fic.write("Vel 3 {} float\n".format(Np))
    for line in Data :
        fic.write("{} {} {} ".format(line[3],line[4],line[5]))
        
    fic.write("\nRhop 1 {} float\n".format(Np))    
    for line in Data :
        fic.write("{} ".format(line[6]))
        
    fic.write("\nMass 1 {} float\n".format(Np))
    for line in Data :
        fic.write("{} ".format(line[7]))
    
    fic.write("\nPress 1 {} float\n".format(Np))
    for line in Data :
        fic.write("{} ".format(line[8]))
        
    fic.write("\nType 1 {} unsigned_char\n".format(Np))
    for line in Data :
        fic.write("{} ".format(int(line[9])))
        
    fic.write("\nCellOffSpring 1 {} unsigned_int\n".format(Np))
    for line in Data :
        fic.write("{} ".format(int(line[10])))
        
    fic.write("\nGradVel 1 {} float\n".format(Np))
    for line in Data :
        fic.write("{} ".format(line[11]))
        
    fic.write("\nVonMises3D 1 {} float\n".format(Np))
    for line in Data :
        fic.write("{} ".format(line[21]))        
    
    fic.write("\nStrainDot 3 {} float\n".format(Np))
    for line in Data :
        fic.write("{} {} {} ".format(line[18],line[19],line[20]))        
    
    # Write tensor data
    fic.write("\nTENSORS Deformation float\n")    
    for line in Data :
        Q = np.array([[line[12],line[13],line[14]],[line[13],line[15]\
                      , line[16]],[line[13],line[16],line[17]]], dtype=float)
        Qi = computeTransformedMatrix(Q)
        fic.write("{} {} {} {} {} {} {} {} {} ".format(\
            Qi[0,0],Qi[0,1],Qi[0,2],Qi[1,0],Qi[1,1],Qi[1,2],\
            Qi[2,0],Qi[2,1],Qi[2,2]))   
    
    #from numpy.linalg import inv
    """for i in range(0,Np):
        Qi = computeTransformedMatrix(\
            np.array([[Csv0['Qfxx'][i], Csv0['Qfxy'][i], Csv0['Qfxz'][i]]\
                      , [Csv0['Qfxy'][i],Csv0['Qfyy'][i],Csv0['Qfyz'][i]]\
                      , [Csv0['Qfxz'][i],Csv0['Qfyz'][i],Csv0['Qfzz'][i]]]))     
        appT(fic,Qi[0,0],Qi[0,1],Qi[0,2]\
         ,Qi[1,0],Qi[1,1],Qi[1,2]\
         ,Qi[2,0],Qi[2,1],Qi[2,2]) """
    
    # End
    fic.close() 
    #print(caseName + "_Avg_{:04d}.vtk created".format(n) )  
    toc = time.perf_counter()
    #print(f"Computation in {toc - tic:0.4f} seconds")
    print(caseName + \
          f"_Avg{Navg}_{n:04d}.vtk done ({(toc - tic)*((Nfiles)/(n+1)-1):0.4f} s remains)")


