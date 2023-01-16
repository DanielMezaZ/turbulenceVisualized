#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 14.01.23

@author: Daniel Meza
"""
# Importing libraries
import numpy as np
import os
from pathlib import Path
# Important the simulation runs using OpenFOAM 6

# Copy simulation setup into the simulationFiles directory \
    # with the target parameters

#Create array with ranges for angle
workDir=os.getcwd()
workDir=str(Path(workDir).parents[1])
sample = np.linspace(0,8.5,30)
ReArray=100*2**sample
sigma=1
U_bulk=1
nuArray=2*sigma*U_bulk/ReArray
for i in range(sample.size):
    #Copy template folder into directory
    src=workDir+"/Code/BaseModel"
    simName="E"+str(i)+"_Re"+str(int(round(ReArray[i],0)))
    dst=workDir+"/Data/SimulationFiles/"+simName
    command="cp -r "+src+" "+dst
    #Execute command
    os.popen(command).read()
    #Open target file
    file = Path(dst+"/config")
    #Change the paramter to the desired value
    nuVal=format(nuArray[i],'.3e')
    file.write_text(file.read_text().replace('inputNuVar', str(nuVal)))
