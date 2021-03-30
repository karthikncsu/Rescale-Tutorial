import requests
import json
import pprint
import sys
import dotenv
import os
from rescale_restapi import BatchJobSubmit
import time
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

def jobdata(file_id,numproc):

  command="cd Sampling-from-high-dimensional-space\n"
  command=command+"cd code\n"
  command=command+'conda install -y mpi4py \nmpirun -np '+str(numproc)+' python sampler.py alloy.txt alloy.out 20000 SMC'

  data={
      'name': 'Intern assignment sampling '+str(numproc),
      "projectId":'gxzXS',
      'jobanalyses': [
        {
          'useMpi': True,
          'command': command,
          'analysis': {
            'code': 'anaconda',
            'version': '5.3.1'
          },
          'hardware': {
            'coresPerSlot': numproc,
            'slots': 1,
            'coreType': 'hpc-3'
          },
          'inputFiles': [
            {
              'id': file_id
            }
          ]
        }
      ]
    }

  return data

input_file='Sampling-from-high-dimensional-space.zip'


jobsobj=BatchJobSubmit()
status_input=jobsobj.file_upload(input_file)
if status_input:
    for numproc in [1,2,4,8,18,36]:
        data=jobdata(jobsobj.file_ids[0],numproc=numproc)
        status_submit=jobsobj.setup_submit_job(data)

jobsobj.status_job()

all_proc_data=[]
for job_id in jobsobj.job_ids:
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
