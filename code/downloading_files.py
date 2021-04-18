import requests
from contextlib import closing

import requests
import json
import pprint
import sys
import dotenv
import os
from datetime import datetime
import time
from rescale_restapi import BatchJobSubmit
import numpy as np
import matplotlib.pyplot as plt

jobsobj=BatchJobSubmit()
job_ids=["ihbAm","gQhOa"]

all_proc_data=[]
for job_id in job_ids:
    status,data=jobsobj.download_file("comp_time.log",job_id)
    if status:
        all_proc_data.append(data[0].split())
        
print(all_proc_data)
if len(all_proc_data)>0:
    all_proc_data=np.asarray(all_proc_data).astype(np.float64)

    fig=plt.figure()
    plt.plot(all_proc_data[:,0],all_proc_data[0,1]/all_proc_data[:,1],"o-")
    plt.xlabel("Number of processors")
    plt.ylabel("Speed up")
    fig.savefig("speedup.png")
    plt.close()

    fig=plt.figure()
    plt.plot(all_proc_data[:,0],all_proc_data[0,1]/(all_proc_data[:,1]*all_proc_data[:,0]),"o-")
    plt.xlabel("Number of processors")
    plt.ylabel("Efficiency")
    fig.savefig("efficiency.png")
    plt.close()

    fig=plt.figure()
    plt.plot(all_proc_data[:,0],all_proc_data[:,1],"o-")
    plt.xlabel("Number of processors")
    plt.ylabel("Computational time (sec)")
    fig.savefig("comptime.png")
    plt.close()
