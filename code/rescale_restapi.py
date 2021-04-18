import requests
import json
import pprint
import sys
import dotenv
import os
from datetime import datetime
import time
import requests
from contextlib import closing
import numpy as np

class BatchJobSubmit:

  def __init__(self):
    """
    code setup
    """
    dotenv.load_dotenv()
    self.myapi_token=os.getenv('myapi_token')
    self.file_ids=[]
    self.job_ids=[]
  
  def known_jobids(self,job_ids):
    for id in job_ids:
      self.job_ids.append(id)
  
  def print_status(self,respo,msg):
    """
    status code of the job
    """
    status_code=respo.status_code
    msg=msg+": "+str(status_code)+" "+requests.status_codes._codes[status_code][0]
    print(msg)
    if status_code==400 or status_code==404:
      pprint.pprint(json.loads(respo.text))
      print('Not going forward with the action')
      return False
    else:
      return True

  def file_upload(self,input_file,oncloud=False):
    """
    Function for uploading input files
    """
    if oncloud:
      self.file_ids.append(file_id)
      return True,file_id
    else:
      #Uploading a file to teh rescale cloud
      file_upload = requests.post(
        'https://platform.rescale.com/api/v2/files/contents/',
        data=None,
        files={'file': open(input_file,'rb')},
        headers={'Authorization': self.myapi_token} 
      )

      status=self.print_status(file_upload,"File upload status")
      if status:
        upload_details=json.loads(file_upload.text)
        file_id=upload_details["id"]
        print("File ID:",file_id)
        self.file_ids.append(file_id)
        return status
      else:
        return status

  def setup_submit_job(self,data):
    """
    Function for setting up and submitting the job
    """

    job_setup=requests.post(
      'https://platform.rescale.com/api/v2/jobs/',
      json=data,
      headers={'Content-Type': 'application/json',
              'Authorization': self.myapi_token}
    )

    status=self.print_status(job_setup,"Job setup status")
    if status:
      job_details=json.loads(job_setup.text)
      job_id=job_details["id"]
      print("Job ID:",job_id)

      job_submit=requests.post(
        'https://platform.rescale.com/api/v2/jobs/%s/submit/'%job_id,
        headers={'Content-Type': 'application/json',
                'Authorization': self.myapi_token}
      )

      status=self.print_status(job_submit,"Job submiting status")
    
    if status:
      self.job_ids.append(job_id)
    else:
      self.job_ids.append(None)      
    return status

  def status_ind_job(self):
    """
    Function for status of all submitted jobs
    """

    job_statuses=[]
    for job_id in self.job_ids:
      if job_id is not None:

        job_status=requests.get(
          'https://platform.rescale.com/api/v2/jobs/%s/statuses/'%job_id,
          headers={'Content-Type': 'application/json',
                  'Authorization': self.myapi_token})

        output_json=json.loads(job_status.text)
        status=output_json["results"][0]["status"]
        job_statuses.append(status)

        statusReason=output_json["results"][0]["statusReason"]
        print("Job Id:",job_id,", Status:",job_statuses[-1],", StatusReason:",statusReason)

      else:
        job_statuses.append("Completed")

    return job_statuses

  def status_job(self):
    """
    Output for status of all the jobs
    """
    while True:
      time.sleep(15)
      
      print("---------",datetime.now(),"----------")
      if len(self.job_ids)==0:
        break
      job_statuses=self.status_ind_job()
      if job_statuses.count('Completed')==len(job_statuses):
        break

  def download_file(self,filename,job_id):
    """
    Download files from job numbers
    """

    #Finding all the url to download the files
    url='https://platform.rescale.com/api/v2/jobs/%s/files/'%job_id
    headers={'Authorization': self.myapi_token}

    file_download=requests.get(url, headers=headers)
    status=self.print_status(file_download,"File download status")
    file_found=False

    if status:
      job_details=json.loads(file_download.text)
      
      while True:
        #Get all the details of the files in the current page
        for arg in job_details["results"]:
          if arg["name"]==filename:
            file_found=True
            downloadUrl=arg["downloadUrl"]

            filename_save="./../downloads/out_"+job_id+"_"+filename
            fout=open(filename_save,"wb")
            with closing(requests.get(downloadUrl, headers=headers, stream=True)) as r:
              with open(filename, 'r') as f:
                for chunk in r.iter_content(chunk_size=100):
                    fout.write(chunk)
            fout.close()
            fout=open(filename_save,"r")
            data=fout.readlines()
            fout.close()
            return True,data        
        
        #Checking for details of the files in the next page
        if job_details["next"]==None:
          break
        url=job_details["next"]

        file_download=requests.get(url, headers=headers)
        job_details=json.loads(file_download.text)
    
      return False,None


      