# -*- coding: utf-8 -*-
"""
Release on 08/06/2020
0806 - Return average along with the standard error
0608 - Introduction of Beemster Data
@author: MM42910
"""

import numpy as np
import csv, os, time
import matplotlib.pyplot as plt

### -1 Def functions
def stats(d):
    sig = dict.fromkeys(d.keys(), 0.0)    
    avg = dict.fromkeys(d.keys(), 0.0)  
    avg2 = dict.fromkeys(d.keys(), 0.0)
    for item in d.keys():
        loc_avg = 0;
        loc_avg2 = 0;
        n = 0;
        for val in d[item]:
            loc_avg += val;
            loc_avg2 += val**2;
            n += 1;
        if n != 0:
            avg[item] = loc_avg/n  
            avg2[item] = loc_avg2/n
    sig = [np.sqrt(abs(avg2[id]-avg[id]**2)/75.0) for id in d.keys()]
    return avg, sig


def procPos(l,b):
    maxPos = 0.0
    for item in l:
        # mm to um conversion
        item['Pos.x'] = float(item['Pos.x'])*1000
        maxPos = max(maxPos, item['Pos.x'])
    
    # Change to tip referential
    for item in l:
        item['Pos.x'] = abs(maxPos-item['Pos.x'])

    # Filter ptc out of bins
    l = [item for item in l if item['Pos.x']<b[-1]]
    
    #> Change to bin        
    for ptc in l:
        ptc['Pos.x'] = [pb for pb in b 
            if abs(pb-ptc['Pos.x'])<=binWidth/2][0]
    return l

def generPrevCount(name):
    d = {}
    with open("Csv\\"+name+"_stats.csv") as csvfile:
        next(csvfile)
        next(csvfile)
        next(csvfile)
        dP = []
        rdP = csv.DictReader(csvfile, delimiter=";")
        for row in rdP:
            del row['']
            dP.append(row) 
    Dt = float(dP[1]['Time'])
    for save in dP[:-1]:
        d["Csv\\"+name+"_"+str(dP.index(save)+1).zfill(4)+".csv"] = int(save['Count'])
    d["Csv\\"+name+"_0000.csv"] = int(dP[0]['Count'])        
    return d, Dt

#######################################################################
### 0 Prelude
# Casename and parameters
caseShort = "B1"
options = "l" #Length, division rate, strain

#Smooth details
n_avg = 5

# Beemster data
beel_avg = [10,10,10,10,10,10,10,11,13,15,17,20,25,30,35,40,45,50,55,60,65,70
            ,75,80,90,95,95,95,95,95,95,95,95,95,95,95]
#beel_avg = [10 for i in range(36)]
beel_se = [0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,5,5,5,5,5,5
            ,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10]
bees_avg = [0.04 for i in range(36)]
bees_se = [0.01 for i in range(36)]
beed_avg = [0.04 for i in range(36)]
#######################################################################

#Bin details
binWidth = 25;
binLength = 900;


# File detection - Get Pure name
caseName = [item[:-10] for item in os.listdir('Csv')
    if caseShort in item and "stats" in item][0]
if not os.path.exists("Png"):
   os.mkdir("Png")
if not os.path.exists("Png\\Beemster-"+caseName+"-"+str(n_avg)):
    os.mkdir("Png\\Beemster-"+caseName+"-"+str(n_avg))


opt_len = "l" in options
opt_div = "d" in options
opt_stn = "s" in options
opt_vel = "v" in options
            
# Generate list of Csv names
CsvList = [name for name in os.listdir('Csv') 
    if caseName in name and 'stats' not in name]

# Generate initial Smoothing subset
bins = np.arange(binWidth/2, binLength+binWidth/2,binWidth)
smoSub = {}

tic = time.perf_counter()
tic_loop = time.perf_counter()
for name in CsvList[:n_avg]:
    currentCaseName = "Csv\\"+name    
    with open(currentCaseName) as csvfile:
        next(csvfile)
        next(csvfile)
        next(csvfile)
        dP = []
        rdP = csv.DictReader(csvfile, delimiter=";")
        for row in rdP:
            del row['']
            dP.append(row) 
            
    # process new csv          
    dP = procPos(dP, bins)
    
    # append new csv to subset
#    smoSub.append(dP)
    smoSub[currentCaseName] = dP
    
if opt_div == True:   
    prevCount, Dt = generPrevCount(caseName)

toc_loop = time.perf_counter()
print(f"Generation smoothing subset in {toc_loop - tic_loop:0.4f} s")

### 1 loop
#> Dev - Filter data list
for name in CsvList[n_avg:]:
    ### 10 Initialise var
#    nb = [0] * len(bins)
    lenb = [[] for i in range(len(bins))]
    inb = [0 for i in range(len(bins))]
    divb = [0 for i in range(len(bins))]
    stnb = [[] for i in range(len(bins))]
    velb = [[] for i in range(len(bins))]
    tic_loop = time.perf_counter()
    
    ### 11 Open Smoothing loop
    # read new csv    
    currentCaseName = "Csv\\"+name    
    with open(currentCaseName) as csvfile:
        next(csvfile)
        next(csvfile)
        next(csvfile)
        dP = []
        rdP = csv.DictReader(csvfile, delimiter=";")
        for row in rdP:
            del row['']
            dP.append(row) 
            
    # process new csv          
    dP = procPos(dP, bins)
    
    # append new csv to subset
    smoSub[currentCaseName] = dP
        
    # for loop data in dataSubset
    for sub in smoSub:
        for ptc in smoSub[sub]:
            if opt_len == True:
                lenb[np.where(bins==ptc['Pos.x'])[0][0]].insert(0,2000./np.sqrt(float(ptc['Qfxx'])))
            if opt_stn == True:
                stnb[np.where(bins==ptc['Pos.x'])[0][0]].insert(0,float(ptc['StrainDot.x'])*0.1)
            if opt_div == True:
                inb[np.where(bins==ptc['Pos.x'])[0][0]]+=1
                if int(ptc['Idp'])>=prevCount[sub]:
                    divb[np.where(bins==ptc['Pos.x'])[0][0]]+=1
            
    # 2 Process average
    if opt_len == True:
        len_avg, len_std = stats(dict(zip(bins,lenb)))
    if opt_stn == True:
        stn_avg, stn_std = stats(dict(zip(bins,stnb)))
    if opt_div == True:
        inb = [1 if x==0 else x for x in inb]
        div_avg = [a/b*0.1/Dt for a,b in zip(divb,inb)]
    
    # 3 Plot stats
    # Cell length
    if opt_len == True:
        plt.scatter(bins, len_avg.values())
        plt.scatter(bins, beel_avg)
        plt.errorbar(bins, len_avg.values(), len_std)
        plt.errorbar(bins, beel_avg, beel_se)
        plt.xlim(0, binLength)    
        plt.ylim(0, 85)     
        # Save data and figures
        plt.savefig("Png\\Beemster-"+caseName+"-"+str(n_avg)+"\\Len"+str(n_avg)+"-"+currentCaseName[4:-4]+".png")
        # Clear figure
        plt.clf()  
    
    # Strain rate
    if opt_stn == True:
        plt.scatter(bins, stn_avg.values())
        plt.errorbar(bins, stn_avg.values(), stn_std)
        plt.xlim(0, binLength)    
        plt.ylim(0, 0.4)     
        # Save data and figures
        plt.savefig("Png\\"+caseName+"-"+str(n_avg)+"\\Stn"+str(n_avg)+"-"+currentCaseName[4:-4]+".png")
        # Clear figure
        plt.clf()  
    
    # Division rate
    if opt_div == True:
        plt.scatter(bins, div_avg)
        plt.xlim(0, binLength)    
        plt.ylim(0, 0.1)     
        # Save data and figures
        plt.savefig("Png\\"+caseName+"-"+str(n_avg)+"\\Div"+str(n_avg)+"-"+currentCaseName[4:-4]+".png")
        # Clear figure
        plt.clf()  
    
    
    # 4 End of loop
    nameDel = [name for name in smoSub.keys() if str(int(currentCaseName[-8:-4])-n_avg).zfill(4) in name][0]
    del smoSub[nameDel]
    toc_loop = time.perf_counter()
    print(currentCaseName[4:-4]+f" processed in  {toc_loop - tic_loop:0.4f} s")

# End of script
toc = time.perf_counter()
print(f"Processed achieved in  {toc - tic:0.4f} s")
    
