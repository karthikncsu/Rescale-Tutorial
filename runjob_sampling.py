import requests
import json
import pprint
import sys
import dotenv
import os
from rescale_restapi import BatchJobSubmit
import time
from datetime import datetime

def jobdata(file_id,numproc):

  command="cd Sampling-from-high-dimensional-space\n"
  command=command+"cd code\n"
  command=command+'conda install -y mpi4py \nmpirun -np '+str(numproc)+' python sampler.py alloy.txt alloy.out 100 SMC'

  data={
      'name': 'Sampling',
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
  data=jobdata(jobsobj.file_ids[0],numproc=8)
  status_submit=jobsobj.setup_submit_job(data)

  data=jobdata(jobsobj.file_ids[0],numproc=18)
  status_submit=jobsobj.setup_submit_job(data)

jobsobj.status_job()