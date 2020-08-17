# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 15:21:56 2020

@author: MM42910
"""
import os, struct, time

### 0 Prelude
# Casename and parameters - local
caseShort = "A2"

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
    
    
print('Vel')
print(struct.unpack(">f", velHdle[:4]))
print(struct.unpack(">f", velHdle[-4:]))
print('Rhop')
print(struct.unpack(">f", rhoHdle[:4]))
print(struct.unpack(">f", rhoHdle[424:428]))
print(struct.unpack(">f", rhoHdle[-4:]))

### Write file

fic = open("..\\Outputs\\Gen_A2_0010.vtk", "wb")
tic = time.perf_counter()
fic.write(b'# vtk DataFile Version 3.0\n')
fic.write(b'Generate single particle for Paraview read\n')
fic.write(b'BINARY\n')
fic.write(b'DATASET POLYDATA\n')
fic.write(b'POINTS 1 float\n')
px = pointsHdle[0:4]
py = pointsHdle[4:8]
pz = pointsHdle[8:12]
fic.write(bytes(px))
fic.write(bytes(py))
fic.write(bytes(pz))
fic.write(b'\n')
fic.write(b'VERTICES 1 2\n')
fic.write(struct.pack(">i", 1))
fic.write(struct.pack(">i", 0))
fic.write(b'\n')
fic.write(b'POINT_DATA 1\n')
fic.write(b'SCALARS Idp unsigned_int\n')
fic.write(b'LOOKUP_TABLE default\n')
fic.write(b'\x00\x00\x00\x00')
fic.write(b'\n')
fic.write(b'FIELD FieldData 1\n')
fic.write(b'Rhop 1 1 float\n')
fic.write(struct.pack(">f", 1000))

toc = time.perf_counter()
print(f"Gen_A2_0010 complete: {toc - tic:0.4f} s")
fic.close()