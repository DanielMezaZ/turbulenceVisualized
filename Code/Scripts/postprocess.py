#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 14.01.23

@author: Daniel Meza
"""
# Importing libraries
import numpy as np
import os
import pandas as pd
from pathlib import Path
from matplotlib import pyplot as plt
# from scipy.spatial import Delaunay
# from stl import mesh  # Need to install library

#Create array with ranges for angle
workDir=os.getcwd()
workDir=str(Path(workDir).parents[1])
sample = np.linspace(0,8.5,30)
ReArray=100*2**sample

# Move one folder down
u=[]
x=[]
Re=[]
for i in range(sample.size):
    simName="E"+str(i)+"_Re"+str(int(round(ReArray[i],0)))
    pathSim=workDir+"/Data/Raw/"+simName
    simFile=pathSim+"/center_y.csv"
    df=pd.read_csv(simFile,delimiter=",")
    x0=np.array(df.iloc[:,0])
    u0=np.array(df.iloc[:,1])
    u=np.append(u,u0)
    x=np.append(x,x0)
    Re=np.append(Re,ReArray[i]*np.ones(2*x0.size))
    for j in range(x0.size):
         x=np.append(x,x[-1]+x0[1])
         u=np.append(u,u0[-j-1])
    # Use to plot individual profiles
    #plt.scatter(x0,u0,label=str(i))
## Add legend to individual profiles
#plt.legend()

logRe=np.log10(Re)

## Scatter plot
#ax = plt.axes(projection='3d')
#ax.scatter(x, logRe, u, c= u, cmap='coolwarm', linewidth=1);

# Triangle plot
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
surf = ax.plot_trisurf(x, logRe, u, cmap='coolwarm', linewidth=0)
ax.set_title("Channel flow: RANS, k-omega SST",fontsize=15)
ax.set_xlabel(r'$y/\delta$',fontsize=8)
ax.set_ylabel(r'$log_{10}(Re_b)$',fontsize=8)
ax.set_zlabel(r'$u/U_b$',fontsize=8)
ax.tick_params(axis='both', which='major', labelsize=6)
ax.tick_params(axis='both', which='minor', labelsize=6)
elevVar=np.array([  0, 20,20,20, 0,90,45])
azimVar=np.array([-90,-45, 0,45,90, 0,45])
for i in range(elevVar.size):
    ax.view_init(elev=elevVar[i], azim=azimVar[i])
    fig.savefig(f"ResponseSurf_{elevVar[i]}_{azimVar[i]}.png",dpi=250)
plt.show()
# # Export plot to stl file (need to fix, as it will not have a volume)
# # Objective: 3D print the plot
# # Solution: Use Meshmixer and extrude all the phases

# # Create triangles
# inputData=np.array([x,logRe]).T
# tri = Delaunay(inputData)
# tris=tri.simplices

# fig = plt.figure()
# ax = fig.add_subplot(1, 1, 1, projection='3d')

# # The triangles in parameter space determine which x, y, z points are
# # connected by an edge
# ax.plot_trisurf(x, logRe, u, triangles=tri.simplices, cmap=plt.cm.Spectral)
# plt.show()

# # Create mesh
# data = np.zeros(len(tris), dtype=mesh.Mesh.dtype)
# mobius_mesh = mesh.Mesh(data, remove_empty_areas=False)
# mobius_mesh.x[:] = x[tris]
# mobius_mesh.y[:] = logRe[tris]
# mobius_mesh.z[:] = u[tris]
# mobius_mesh.save('iLoveCFD_V2.stl')

# # TODO: Compute shear stresses as a function of Reb