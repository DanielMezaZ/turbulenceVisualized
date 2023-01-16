import pandas as pd 
from matplotlib import pyplot as plt
import numpy as np
import os.path
import subprocess
import argparse
import math
from pathlib import Path

def calcParams(params):
    [u_b,delta,nu,Re]=params
    paramsLabel=["Ubar","sigma","nuVar","Re_b"]
    unknownsNo=0
    for i in range(params.size):
        if params[i]==None or math.isnan(params[i]):
            unknownsNo=unknownsNo+1    
    if unknownsNo==1:        
        for i in range(params.size):
            if params[i]==None or math.isnan(params[i]):
                print(f"Solve for {paramsLabel[i]}")   
                if paramsLabel[i]==paramsLabel[0]:
                    params[0]=params[3]*params[2]/(2*params[1])
                if paramsLabel[i]==paramsLabel[1]:
                    params[1]=params[3]*params[2]/(2*params[0])
                if paramsLabel[i]==paramsLabel[2]:
                    params[2]=2*params[0]*params[1]/(params[3])
                if paramsLabel[i]==paramsLabel[3]:
                    params[3]=2*params[0]*params[1]/(params[2])       
    elif unknownsNo==0:
        if params[3]!=2*params[0]*params[1]/params[2]:
            print("Error: Parameters do not match")
    elif unknownsNo>1:
        print("Error: Too many unkowns")
    return params

# params=u_b,delta,nu,Re] - default values
params=np.array([1,0.5,1,None])
      
parser = argparse.ArgumentParser()
parser.add_argument('-Ubar', dest='Ubar', action='store')
parser.add_argument('-delta', dest='delta', action='store')
parser.add_argument('-nu', dest='nu', action='store')
parser.add_argument('-Re_b', dest='Re_b', action='store')
args = parser.parse_args()
#print(args.Ubar)
if args.Ubar!=None:
    if args.Ubar=="None":
        params[0]=None
    else:
        params[0]=float(args.Ubar)
if args.delta!=None:
    if args.delta=="None":
        params[1]=None
    else:
        params[1]=float(args.delta)
if args.nu!=None:
    if args.nu=="None":
        params[2]=None
    else:
        params[2]=float(args.nu)
if args.Re_b!=None:
    if args.Re_b=="None":
        params[3]=None
    else:
        params[3]=float(args.Re_b)

#print(params)
params=calcParams(params)
# Run again to verify
params=calcParams(params)
print(f"Ubar: {params[0]}; delta: {params[1]}; nu: {params[2]}; Re_b: {params[3]}")

#Create array with ranges for angle
workDir="/home/jdmezazeron/gitDanielMezaZ/turbulenceVisualized/Code/SimExec"
print("Working directory: "+workDir)
f=open(workDir+"/config","w")
#Change the paramter to the desired value
paramsLabel=["Ubar","sigma","nuVar","Re_b"]
for i in range(params.size-1):
    paramVal=format(params[i],'.3e')
    f.write(f"{paramsLabel[i]}\t{paramVal};\n")

f.write("nCellsX\t4;\n")
f.write("nCellsY\t50;\n")
f.write("wallGrading\t4.0;\n")
f.write("endTime\t5000;\n")
f.close()

command=workDir+"/Allclean"
p = subprocess.Popen(command,cwd=workDir)
p.wait()
command=workDir+"/Allrun"
p = subprocess.Popen(command,cwd=workDir)
p.wait()
command="sudo find "+workDir+"/postProcessing -mindepth 2 -type f -exec mv -f '{}' "+workDir+"/postProcessing ';'"
p = subprocess.call(command, shell=True,cwd=workDir)

simFile=workDir+"/postProcessing/center_y.csv"
df=pd.read_csv(simFile,delimiter=",")
y0=np.array(df.iloc[:,0])
u0=np.array(df.iloc[:,1])
u=u0
y=y0
for j in range(y0.size):
      y=np.append(y,y[-1]+y0[1])
      u=np.append(u,u0[-j-1])
plt.plot(y,u)
plt.xlabel("Distance to wall")
plt.ylabel("Velocity")
plt.title(f"u_b: {params[0]}; delta: {params[1]}; nu: {params[2]}; Re_b: {params[3]}")
plt.tight_layout()
plt.savefig("channelVelProfPlot.png",dpi=250)

f=open("channelVelProf.csv","w")
for i in range(y.size):
    yVal=format(y[i],'.3E')
    uVal=format(u[i],'.3E')
    f.write(f"{yVal},{uVal}\n")
f.close()