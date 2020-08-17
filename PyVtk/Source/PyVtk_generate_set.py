# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 15:21:56 2020

@author: MM42910
"""
import os, struct, time

### 0 Prelude
# Casename and parameters - local
caseShort = "A2"

N = 2975
F = 2

# Directory generation - local
if not os.path.exists("..\\Outputs"):
    os.mkdir("..\\Outputs")
   
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

### Write file
fic = open("..\\Outputs\\Bin_A2_0010.vtk", "wb")
tic = time.perf_counter()
fic.write(b'# vtk DataFile Version 3.0\n')
fic.write(b'Generate single particle for Paraview read\n')
fic.write(b'BINARY\n')
fic.write(b'DATASET POLYDATA\n')
fic.write(b'POINTS '+bytes(str(N), 'utf-8')+b' float\n')
fic.write(pointsHdle+b'\n')
#fic.write(
# struct.pack(">f", -0.22)+struct.pack(">f", 0.01)+struct.pack(">f", -0.38)+b'\n')
fic.write(b'VERTICES '+bytes(str(N), 'utf-8')+b' '+bytes(str(2*N), 'utf-8')+b'\n')
fic.write(vertHdle+b'\n')
fic.write(b'POINT_DATA '+bytes(str(N), 'utf-8')+b'\n')
fic.write(b'SCALARS Idp unsigned_int\n')
fic.write(b'LOOKUP_TABLE default\n')
fic.write(lookHdle+b'\n')
fic.write(b'FIELD FieldData '+bytes(str(F), 'utf-8')+b'\n')
fic.write(b'Vel 3 '+bytes(str(N), 'utf-8')+b' float\n')
fic.write(velHdle+b'\n')
fic.write(b'Rhop 1 '+bytes(str(N), 'utf-8')+b' float\n')
fic.write(rhoHdle+b'\n')

toc = time.perf_counter()
print(f"Bin_A2_0010 complete: {toc - tic:0.4f} s")
fic.close()