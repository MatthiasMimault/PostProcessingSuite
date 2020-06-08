# -*- coding: utf-8 -*-
"""
Created on 27/05/20
Averaging procedure, CSV-CSV
"""

import numpy as np
import struct as s
import csv, os, time
#import math
import sys

os.chdir(".")

""" I. Definition functions """
def searchCsv(short,path):
    #Pending: try error if empty, flexible selection of files
    listOfFiles = os.listdir(path)
    #try if casename is empty
    caseName = [entry[:-10] for entry in listOfFiles 
        if "stats" in entry and caseShort in entry]
    return [name for name in listOfFiles 
        if caseName[0] in name and 'stats' not in name]
    
def readCsv(name):
    with open(name) as csvfile:
        next(csvfile)
        next(csvfile)
        next(csvfile)
        dP = []
        # Csv extraction
        rdP = csv.DictReader(csvfile, delimiter=";")
        for row in rdP:
            del row['']
            dP.append(row)
        # File renumbering by particle IDs
        return {i : d for i, d in [[int(line['Idp']), line] for line in dP] }
        
        # Convert fields to float and int
        
def writeCsv(name, data):
    with open(name, 'w', newline='\n') as f:
        w = csv.DictWriter(f,delimiter=";",fieldnames=data[0].keys())
        #> Skip three lines
        w.writeheader()
        for index in data:
            w.writerow(data[index])
            
def writeVtk(name, data):
    Np = len(data)
    fsca = [item for item in data[0].keys() if '.' not in item 
               and 'Qf' not in item and ': ' not in item]
    fvec = [item[:-2] for item in data[0].keys() 
                if '.x' in item and 'Pos' not in item]
    ften = [item[:-2] for item in data[0].keys() if 'xx' in item]
        
    with open(name[:-4]+'.vtk', 'w') as f:
        f.write("# vtk DataFile Version 3.0\nTest VTK file for Force data\n"+
            "BINARY\nDATASET POLYDATA\nPOINTS {} float\n".format(Np))  
    
    with open(name[:-4]+'.vtk', 'ab') as f:    
        w = b""  
        for id in data:
            w += s.pack('>fff'
                , float(data[id]['Pos.x'])
                , float(data[id]['Pos.y'])
                , float(data[id]['Pos.z']))        
        f.write(w)
        
    with open(name[:-4]+'.vtk', 'a') as f:
        f.write("VERTICES {} {}\n".format(Np, Np*2))
        
    with open(name[:-4]+'.vtk', 'ab') as f:   
        w = b""          
        i = 0
        for id in data:
            w += s.pack('>ii', 1, i)    
        f.write(w)
        
        
    with open(name[:-4]+'.vtk', 'a') as f:
        f.write("\nPOINT_DATA {}\nSCALARS Idp unsigned_int\nLOOKUP_TABLE default\n".format(Np))
    
    with open(name[:-4]+'.vtk', 'ab') as f:   
        w = b""      
        for id in data:
            w += s.pack('>i', int(data[id]['Idp']))   
        f.write(w) 
        
    with open(name[:-4]+'.vtk', 'a') as f:
        f.write("FIELD FieldData {}\n".format(len(fsca)+len(fvec)))
        
    # Scalar loop
    for item in fsca:  
        with open(name[:-4]+'.vtk', 'a') as f:          
            f.write("{} {} {} {}\n".format(item, 1, Np, "float"))
            
        with open(name[:-4]+'.vtk', 'ab') as f:   
            w = b""      
            for id in data:
                w += s.pack('>f', float(data[id][item]))   
            f.write(w) 
            
        with open(name[:-4]+'.vtk', 'a') as f:          
            f.write("\n")
            f.flush()
    
    # Vector loop
    for item in fvec:  
        with open(name[:-4]+'.vtk', 'a') as f:          
            f.write("{} {} {} {}\n".format(item, 3, Np, "float"))
            
        with open(name[:-4]+'.vtk', 'ab') as f:   
            w = b""      
            for id in data:
                w += s.pack('>fff', float(data[id][item+".x"])
                    , float(data[id][item+".y"]), float(data[id][item+".z"]))   
            f.write(w) 
            
        with open(name[:-4]+'.vtk', 'a') as f:          
            f.write("\n")
            f.flush()
    
    # Tensor loop
     
def defineFields(dic):
    return [field for field in dic.keys() 
        if 'Ace' in field or 'Gradv' in field or 'Strain' in field
        or 'Press' in field or 'Vel' in field or 'VonM' in field
        or 'Rhop' in field]
    
def initiateHandle(N, f):
    h = {}
    for i in range(N):
        h[i] = {}
        for field in f:
            h[i][field] = 0.0
    return h


""" II. Main """
### 0. Prelude
# Casename and parameters
caseShort = "A2"
N0 = 0
NF = 10
Navg = 1

# Directory generation
if not os.path.exists("..\\Output"):
    os.mkdir("..\\Output")

# Generate list of Csv names
CsvList = searchCsv(caseShort,'..\\Csv\\')
# Filter CsvList with range of interest
Nfiles = len(CsvList)

# Start global timer
tic = time.perf_counter()

### 1. Global loop
# Prepare the initial working list
fileSubset = []
for file in CsvList[N0-Navg:N0-1]:
    currentName = "..\\Csv\\"+file
    fileSubset.append(readCsv(currentName))
    # fix the missing files that are before Nmin (non-existent or filtered) 
    # fix the missing fields due to cell division, correct value 

# File loop
for file in CsvList[N0:NF]:
    currentName = "..\\Csv\\"+file
    writeName = "..\\Output\\Avg"+file[1:]
    tic_loop = time.perf_counter()
    
    # add new element in avg subset
    fileSubset.append(readCsv(currentName))  
      
    #> fix the missing fields due to cell division, correct value
    
    # initiate the temporary handle (dictionary size particles x fields)
    fields = defineFields(fileSubset[0][0])
    temp = initiateHandle(len(fileSubset[0]), fields)
#    for field in fields:
#        temp[field] = 0.0
    
    # average over the list fileSubset
    for sub in fileSubset:
        for ptc in sub:
            for field in fields:
                temp[ptc][field] += float(sub[ptc][field])/Navg
    handle = fileSubset[0]
    for ptc in handle:
        for field in fields:
            handle[ptc][field] = temp[ptc][field]
    
    
    # write a csv file renumbered
    writeCsv(writeName, handle)
    writeVtk(writeName, handle)
    
    # pop out the first element of the avg subset
    fileSubset.pop(0)
    toc_loop = time.perf_counter()
    print(file+f" processed in  {toc_loop - tic_loop:0.4f} s")
    
#> write a new csv_stats
toc = time.perf_counter()
print(f"Processed achieved in  {toc - tic:0.4f} s")
