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

dotenv.load_dotenv()
myapi_token=os.getenv('myapi_token')

import requests
from contextlib import closing

url='https://platform.rescale.com/api/v2/jobs/ihbAm/files/'
headers={'Authorization': myapi_token}

job_status=requests.get(url, headers=headers)

output_json=json.loads(job_status.text)

print(output_json["results"][0]["downloadUrl"])

url_down=output_json["results"][0]["downloadUrl"]
file_name=output_json["results"][0]["name"]

url_down='https://platform.rescale.com/api/v2/files/kxjeNf/contents/'

fout=open('comp_time.log',"wb")
with closing(requests.get(url_down, headers=headers, stream=True)) as r:
  with open('comp_time.log', 'r') as f:
    for chunk in r.iter_content(chunk_size=100):
        print(chunk)
        fout.write(chunk)

fout.close()



# jobsobj=BatchJobSubmit()
# jobsobj.known_jobids(["mytCgb"])

# jobsobj.status_job()