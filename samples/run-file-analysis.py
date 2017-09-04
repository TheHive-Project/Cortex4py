#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
from cortex4py.api import CortexApi
from cortex4py.api import CortexException


api = CortexApi('http://127.0.0.1:9000')

print('Run analyzer')
print('-----------------------------')
try:
    job_id = None
    response = api.run_analyzer("File_Info_2_0", "file", 1, "./sample.txt")
    print(json.dumps(response, indent=4, sort_keys=True))
    print('')
    job_id = response["id"]
except CortexException as ex:
    print('[ERROR]: Failed to run file analyzer: {}'.format(ex.message))
    sys.exit(0)

print('Get Job Report')
print('-----------------------------')
try:
    response = api.get_job_report(job_id)

    status = response["status"]
    print(json.dumps(response, indent=4, sort_keys=True))
    print('')
except CortexException as ex:
    print('[ERROR]: Failed to get job report'.format(ex.message))
    sys.exit(0)
