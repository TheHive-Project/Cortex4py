#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
from cortex4py.api import CortexApi
from cortex4py.api import CortexException

api = CortexApi('http://127.0.0.1:9000')

print('List all analyzers')
print('-----------------------------')

try:
    response = api.get_analyzers()
    print('{} analyzers found'.format(len(response)))
    print(json.dumps(response, indent=4, sort_keys=True))
    print('')
except CortexException as ex:
    print('[ERROR]: Failed to list analyzers ({})'.format(ex.message))
    sys.exit(0)

print('List analyzers for file observables')
print('-----------------------------')

try:
    response = api.get_analyzers("ip")
    print('{} analyzers found for ip observables'.format(len(response)))
    print(json.dumps(response, indent=4, sort_keys=True))
    print('')
except CortexException as ex:
    print('[ERROR] Failed to list analyzers for ip observables ({})'.format(ex.message))
    sys.exit(0)
