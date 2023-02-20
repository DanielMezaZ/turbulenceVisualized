#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 14.01.23

@author: Daniel Meza
"""
# IMPORTANT: Need to execute from command window as admin
# Executes all the simulationFiles and arranges them in the Data/RAW directory

# Importing libraries
import numpy as np
import subprocess
import os
from pathlib import Path

#Create array with ranges for angle
workDir=os.getcwd()
workDir=str(Path(workDir).parents[1])

sample = np.linspace(0,8,50)
ReArray=100*2**sample

for i in range(sample.size):
    simName="K"+str(i)+"_Re"+str(int(round(ReArray[i],0)))
    pathSim=workDir+"/Data/SimulationFiles/"+simName
    command="./Allrun"
    p = subprocess.Popen(command, cwd=pathSim)
    p.wait()
    command="mkdir ../../Raw/"+simName
    p = subprocess.Popen(command, cwd=pathSim,shell=True)
    p.wait()
    command="cp -r ./postProcessing/sample/* ../../Raw/"+simName
    p = subprocess.call(command, cwd=pathSim,shell=True)

# Move one folder down -latestTime of the simulation is not required
# Only this section needs admin permission
for i in range(sample.size):
    simName="K"+str(i)+"_Re"+str(int(round(ReArray[i],0)))
    pathSim=workDir+"/Data/Raw/"+simName
    command="sudo find "+pathSim+" -mindepth 2 -type f -exec mv -f '{}' "+pathSim+ " ';'"
    p = subprocess.call(command, cwd=pathSim,shell=True)