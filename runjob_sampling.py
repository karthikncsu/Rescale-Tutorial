import requests
import json
import pprint
import sys
import dotenv
import os

def print_status(respo,msg):
    status_code=respo.status_code
    msg=msg+": "+str(status_code)+" "+requests.status_codes._codes[status_code][0]
    print(msg)
    if status_code==400 or status_code==404:
        pprint.pprint(json.loads(respo.text))
        sys.exit('Exiting the job midway')

#------------------------Uploading file-----------------------
dotenv.load_dotenv()
myapi_token=os.getenv('myapi_token')

#Uploading a file
file_upload = requests.post(
  'https://platform.rescale.com/api/v2/files/contents/',
  data=None,
  files={'file': open('sampler.zip','rb')},
  headers={'Authorization': myapi_token} 
)

print_status(file_upload,"File upload status")

#Getting the file id
upload_details=json.loads(file_upload.text)
File_ID=upload_details["id"]
print("File ID:",File_ID)

#------------------------Setting up job-----------------------
#Setting up the data for the job
numproc=4
command='conda install -y mpi4py \nmpirun -np '+str(numproc)+' python sampler/sampler.py alloy.txt alloy.out 5000 SMC'
data={
    'name': 'Intern assignment sampling',
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
            'id': File_ID
          }
        ]
      }
    ]
  }

#Setting the job
job_setup=requests.post(
  'https://platform.rescale.com/api/v2/jobs/',
  json=data,
  headers={'Content-Type': 'application/json',
           'Authorization': myapi_token}
)

print_status(job_setup,"Job setup status")

job_details=json.loads(job_setup.text)
job_ID=job_details["id"]
print("Job ID:",job_ID)

#------------------------Submitting the job-----------------------

job_submit=requests.post(
  'https://platform.rescale.com/api/v2/jobs/%s/submit/'%job_ID,
  headers={'Content-Type': 'application/json',
           'Authorization': myapi_token}
)

print_status(job_submit,"Job submiting status")

#------------------------Status of the job-----------------------
job_status=requests.get(
  'https://platform.rescale.com/api/v2/jobs/%s/statuses/'%job_ID,
  headers={'Content-Type': 'application/json',
           'Authorization': myapi_token}
)

print_status(job_status,"Submitted job status")

# pprint.pprint(json.loads(job_status.text))