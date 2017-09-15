#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
from cortex4py.api import CortexApi
from cortex4py.api import CortexException

api = CortexApi('http://127.0.0.1:9000')

print('Run analyzer')
print('-----------------------------')
job_id = None
try:
    response = api.run_analyzer("MaxMind_GeoIP_3_0", "ip", 1, "8.8.8.8")
    print(json.dumps(response, indent=4, sort_keys=True))
    print('')
    job_id = response["id"]
except CortexException as ex:
    print('[ERROR]: Failed to run analyzer ({})'.format(ex.message))
    sys.exit(0)

print('Get Job Report')
print('-----------------------------')
try:
    response = api.get_job_report(job_id, '30s')
    print(json.dumps(response, indent=4, sort_keys=True))
    print('')
except CortexException as ex:
    print('[ERROR]: Failed to get job report ({})'.format(ex.message))
    sys.exit(0)

print('Delete the job')
print('-----------------------------')
try:
    response = api.delete_job(job_id)
    print('Job has been deleted')
    print('')
except CortexException as ex:
    print('[ERROR]: Failed to delete job ({})'.format(ex.message))
    sys.exit(0)
