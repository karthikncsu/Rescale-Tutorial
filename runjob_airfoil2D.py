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

def jobdata(file_id,projectId):

  data={
      'name': 'Airfoil 2D',
      "projectId":'gxzXS',
      'jobanalyses': [
      {
          'useMpi': False,
          'command': 'cd airfoil2D\n./Allrun',
          'analysis': {
          'code': 'openfoam',
          'version': '2.3.0-openmpi'
          },
          'hardware': {
          'coresPerSlot': 1,
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

dotenv.load_dotenv()
projectId=os.getenv('projectId')

input_file='airfoil2D.zip'

jobsobj=BatchJobSubmit()
status_input=jobsobj.file_upload(input_file)
if status_input:
    for i in range(0,4):
        data=jobdata(jobsobj.file_ids[0],projectId=projectId)
        status_submit=jobsobj.setup_submit_job(data)
jobsobj.status_job()

