#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import time
from cortex4py.api import CortexApi


api = CortexApi('http://127.0.0.1:9000', {'http': '', 'https': ''})

print('Run analyzer')
print('-----------------------------')
job_id = None
response = api.run_analyzer("MaxMind_GeoIP_2_0", "ip", 1, "8.8.8.8")
if response.status_code == 200:
    print(json.dumps(response.json(), indent=4, sort_keys=True))
    print('')
    job_id = response.json()["id"]
else:
    print('ko: {}/{}'.format(response.status_code, response.text))
    sys.exit(0)

print('Get Job Report')
print('-----------------------------')
status = 'InProgress'
while status == 'InProgress':
    response = api.get_job_report(job_id)

    if response.status_code == 200:
        status = response.json()["status"]
        if status == "InProgress":
            time.sleep(1)
        else:
            print(json.dumps(response.json(), indent=4, sort_keys=True))
            print('')
    else:
        print('ko: {}/{}'.format(response.status_code, response.text))
        sys.exit(0)
