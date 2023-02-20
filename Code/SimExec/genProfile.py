import pandas as pd 
from matplotlib import pyplot as plt
import numpy as np
import os.path
import subprocess
import argparse
import math
from pathlib import Path

### NOTICE: Problems reading decimal values for nu. Action: use nu=1
# Run from terminal
exportOmega=False

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
        if np.abs((params[3]-2*params[0]*params[1]/params[2])/params[3])>0.01:
            print("Error: Parameters do not match, undefining Re_b for matching")
            # Undefine Re_b to make them match
            params[3]=None
    elif unknownsNo>1:
        print("Error: Too many unkowns")
    return params

# params=u_b,delta,nu,Re] - default values
params=np.array([1,1,None,9550])
      
parser = argparse.ArgumentParser()
parser.add_argument('-Ubar', dest='Ubar', action='store')
parser.add_argument('-delta', dest='delta', action='store')
parser.add_argument('-nu', dest='nu', action='store')
parser.add_argument('-Re_b', dest='Re_b', action='store')
parser.add_argument('-o', dest='o', action='store')
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
if args.o!=None:
    outputFile=args.o
else:
    outputFile=None
    
#print(params)
params=calcParams(params)
# Run again to verify
params=calcParams(params)

if outputFile == None:
    outputFile=f"u_b_{format(params[0],'.3E')}_delta_{format(params[1],'.3E')}"
    f"_nu_{format(params[2],'.3E')}_Re_b_{format(params[3],'.3E')}"

print(f"Ubar: {params[0]}; delta: {params[1]}; "
      f"nu: {params[2]}; Re_b: {params[3]}")

k0=3/2*(0.16*params[3]**(-1/8)*params[0])**2
omega0=k0**0.5/(0.09**0.25*2*params[1])
#Create array with ranges for angle
workDir="/home/jdmezazeron/gitDanielMezaZ/turbulenceVisualized/Code/SimExec"
print("Working directory: "+workDir)
f=open(workDir+"/config","w")
#Change the paramter to the desired value
paramsLabel=["Ubar","sigma","nuVar","Re_b"]
for i in range(params.size-1):
    paramVal=params[i]
    #paramVal=format(params[i],'.3e')
    f.write(f"{paramsLabel[i]}\t{paramVal};\n")

f.write(f"k0\t{format(k0,'.3E')};\n")
f.write(f"omega0\t{format(omega0,'.3E')};\n")
f.write("nCellsX\t4;\n")
f.write("nCellsY\t50;\n")
f.write("wallGrading\t4.0;\n")
f.write("endTime\t5000;\n")
f.write("writeInt\t1000;\n")
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
k=np.array(df.iloc[:,4])
#nut=np.array(df.iloc[:,5])
u=u0
y=y0

## Full channel
#for j in range(y0.size):
      #y=np.append(y,y[-1]+y0[1])
      #u=np.append(u,u0[-j-1])
      
# Normalize for PaceFish (nondim profile)
y=y/np.max(y)
u_c=np.max(u)
u=u/u_c
k=k/u_c**2

params[1]=1

fig, axs = plt.subplots(nrows=2,ncols=1) 
fig.suptitle(f"U_b: {format(params[0],'.2E')}; delta: {format(params[1],'.2E')};"
          f" nu: {format(params[2],'.2E')}; Re_b: {format(params[3],'.2E')}")

axs[0].plot(y,u,'b')
yref=np.linspace(0, params[1],100)
# Laminar analytical solution
uLam=1*(2*yref-1*yref**2)
axs[0].plot(yref,uLam,'--',color='0.8')
# Turbulent empirical solution
uTur=1*(yref)**(1/7)
axs[0].plot(yref,uTur,'--',color='0.8')
#axs[0].set_title("Ux")
axs[0].set_xlabel(r"y/delta")
axs[0].set_ylabel(r"U_x/U_c")
axs[0].set_ylim([-0.05,1.05])
axs[1].plot(y,k,'b')
#axs[1].set_title("TKE")
axs[1].set_xlabel(r"y/delta")
axs[1].set_ylabel("TKE/U_c^2")
axs[1].set_ylim([-0.001,0.01])
plt.tight_layout()
fig.savefig(f"{outputFile}.png",dpi=250)


f=open(f"{outputFile}.csv","w")
for i in range(y.size):
    yVal=format(y[i],'.3E')
    uVal=format(u[i],'.3E')
    kVal=format(k[i],'.3E')
    f.write(f"{yVal},{uVal},{kVal}\n")
    #nutVal=format(nut[i],'.3E')
    #f.write(f"{yVal},{uVal},{kVal},{nutVal}\n")
f.close()