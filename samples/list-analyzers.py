#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
from cortex4py.api import CortexApi

api = CortexApi('http://127.0.0.1:9000', {'http': '', 'https': ''})

print('List all analyzers')
print('-----------------------------')
response = api.get_analyzers()
if response.status_code == 200:
    print(json.dumps(response.json(), indent=4, sort_keys=True))
    print('')
else:
    print('ko: {}/{}'.format(response.status_code, response.text))
    sys.exit(0)

print('List analyzers for file observables')
print('-----------------------------')
response = api.get_analyzers(dataType="ip")
if response.status_code == 200:
    print(json.dumps(response.json(), indent=4, sort_keys=True))
    print('')
else:
    print('ko: {}/{}'.format(response.status_code, response.text))
    sys.exit(0)