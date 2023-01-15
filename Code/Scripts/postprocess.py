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
from scipy.spatial import Delaunay
from stl import mesh  # Need to install library

#Create array with ranges for angle
workDir=os.getcwd()
workDir=str(Path(workDir).parents[1])
sample = np.linspace(0,8.5,150)
ReArray=100*2**sample

# Move one folder down
u=[]
x=[]
Re=[]
for i in range(sample.size):
    simName="E"+str(i)+"_Re"+str(int(round(ReArray[i],0)))
    pathSim=workDir+"/Data/Raw/"+simName
    simFile=pathSim+"/center_y_U.xy"
    df=pd.read_csv(simFile,delimiter="	",header=None)
    x0=np.array(df[0].to_list())
    u0=np.array(df[1].to_list())
    u=np.append(u,u0)
    x=np.append(x,x0)
    Re=np.append(Re,ReArray[i]*np.ones(2*x0.size))
    for j in range(x0.size):
        x=np.append(x,x[-1]+x0[1])
        u=np.append(u,u0[-j-1])
    ## Use to plot individual profiles
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
ax.set_title("Channel flow: RANS, k-omega SST",fontsize=25)
ax.set_xlabel(r'$y/\delta$',fontsize=20)
ax.set_ylabel(r'$log_{10}(Re_b)$',fontsize=20)
ax.set_zlabel(r'$u/U_b$',fontsize=20)
ax.tick_params(axis='both', which='major', labelsize=10)
ax.tick_params(axis='both', which='minor', labelsize=10)
ax.view_init(elev=90., azim=0)
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