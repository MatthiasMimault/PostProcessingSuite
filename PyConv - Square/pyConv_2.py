# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 09:37:47 2020

@author: MM42910
"""
import matplotlib.pyplot as plt
import os, csv

### -1. Definition of functions
def p(r):
    gamma = 1
    K = 561000
    r0 = 1000
    return K/gamma*(r/r0-1)**gamma
def ex(r):
    nu = 0.3
    E = 785400
    return (1-nu)/E*p(r)
def rs(t):
    r0 = 1000
    rg = 1000
    return r0+rg*t
def readCsv(c):
    with open('Csv\\'+c) as csvfile:
        next(csvfile)
        next(csvfile)
        next(csvfile)
        dP = []
        rdP = csv.DictReader(csvfile, delimiter=";")
        for row in rdP:
            del row['']
            dP.append(row)
    return dP

### 0. Parameters #############################################################
# Short name to load, principal constants
caseShort = "G1b"

###############################################################################

# File detection - Get Pure name
caseName = [item[:-10] for item in os.listdir('Csv')
    if caseShort in item and "stats" in item][0]
if not os.path.exists("Png"):
   os.mkdir("Png")

# Generate list of Csv names
CsvList = [name for name in os.listdir('Csv') 
    if caseName in name and 'stats' not in name]
CsvStat = [name for name in os.listdir('Csv') 
    if caseName in name and 'stats' in name][0]

# Retrieve simulation parameters
dPs = readCsv(CsvStat)

T = float(dPs[-1]['Time'])
dt = float(dPs[1]['Time'])
#T = 0.5
#dt = 0.005

### 1. Analytical solution
#time = [dt*i for i in range(int((T+dt)/dt))]
time = [10*float(dP['Time']) for dP in dPs]
exx = [0.01343 for t in time]
ezz = [0.000118 for t in time]
#ex_array = [ex(rs(t)) for t in time]
#plt.plot(time, ex_array,'-|')

### 2. Approximate solution
dP0 = readCsv(CsvList[0])
Pos0 = {int(dP0[i]['Idp']):float(dP0[i]['Pos.x']) for i in range(len(dP0))
    if abs(float(dP0[i]['Pos.x']))>0.0001}

Poz0 = {int(dP0[i]['Idp']):float(dP0[i]['Pos.z']) for i in range(len(dP0))
    if abs(float(dP0[i]['Pos.z']))>0.0001}
#M0 = sum([float(dP0[i]['Mass']) for i in range(len(dP0))])
#
#dP50 = readCsv(CsvList[50])
#Pos50 = {int(dP50[i]['Idp']):float(dP50[i]['Pos.x']) for i in range(len(dP50))}
#M50 = sum([float(dP50[i]['Mass']) for i in range(len(dP0))])
#
#ex50 = [Pos50[i]/Pos0[i]-1 for i in Pos0.keys()]
#print(ex(M50/M0*1000))

### 3. Retrieve Density, Mass and Deformation
Mb = []
Db = []
Eb = []
Ez = []
for file in CsvList:
    dP = readCsv(file)
    Mb.append(sum([float(dP[i]['Mass']) for i in range(len(dP))])/len(dP))
    Db.append(sum([float(dP[i]['Rhop']) for i in range(len(dP))])/len(dP))
    Pos = {int(dP[i]['Idp']):float(dP[i]['Pos.x']) for i in range(len(dP0))
        if abs(float(dP[i]['Pos.x']))>0.0001}
    Eb.append(sum([Pos[i]/Pos0[i]-1 for i in Pos0.keys()])/len(Pos0))
    Poz = {int(dP[i]['Idp']):float(dP[i]['Pos.z']) for i in range(len(dP0))
        if abs(float(dP[i]['Pos.z']))>0.0001}
    Ez.append(sum([Poz[i]/Poz0[i]-1 for i in Poz0.keys()])/len(Poz0))
    

#plt.figure(0)
#plt.plot(time, Mb,'-|')
plt.figure(1)
plt.plot(time, Db,'-|')
plt.figure(2)
plt.plot(time, Eb,'-|', label=r'$\varepsilon_x$')
plt.plot(time, exx,'tab:blue')
plt.plot(time, Ez,'-|', label=r'$\varepsilon_y$')
plt.plot(time, ezz, 'tab:orange')
plt.xlabel('Time (hours)')
plt.ylabel('Deformation')
plt.legend()

### 3. Error computation 