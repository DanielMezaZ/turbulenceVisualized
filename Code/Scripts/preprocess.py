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
sample = np.linspace(0,8,50)
ReArray=100*2**sample
delta=1
U_bulk=1
nuArray=2*delta*U_bulk/ReArray
for i in range(sample.size):
    #Copy template folder into directory
    src=workDir+"/Code/BaseModel"
    simName="K"+str(i)+"_Re"+str(int(round(ReArray[i],0)))
    dst=workDir+"/Data/SimulationFiles/"+simName
    command="cp -r "+src+" "+dst
    #Execute command
    os.popen(command).read()
    #Open target file
    file = Path(dst+"/config")
    #Change the paramter to the desired value
    k0=3/2*(0.16*ReArray[i]**(-1/8)*U_bulk)**2
    omega0=k0**0.5/(0.09**0.25*2*delta)
    f=open(file,"w")
    #Change the paramter to the desired value
    f.write(f"Ubar\t{U_bulk};\n")
    f.write(f"sigma\t{delta};\n")
    f.write(f"nuVar\t{format(nuArray[i],'.3E')};\n")
    f.write(f"k0\t{format(k0,'.3E')};\n")
    f.write(f"omega0\t{format(omega0,'.3E')};\n")
    f.write("nCellsX\t4;\n")
    f.write("nCellsY\t100;\n")
    f.write("wallGrading\t4.0;\n")
    f.write("endTime\t10000;\n")
    f.write("writeInt\t2500;\n")
    f.close()
