#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import warnings
import json
import os
import magic

try:
    import requests
except Exception as excp:
    warnings.warn("requests library is non installed")


class CortexApi:

    """
        Python API for Cortex

        :param url: Cortex URL
        :param proxies: dict object defining URLs of http and https proxies
    """

    def __init__(self, url, proxies):

        self.url = url
        self.proxies = proxies

    def get_analyzers(self, **args):
        if args.get('dataType', False):
            req = self.url + '/api/analyzer/type/{}'.format(args["dataType"])
        else:
            req = self.url + '/api/analyzer'

        try:
            return requests.get(req, proxies=self.proxies)
        except requests.exceptions.RequestException as e:
            sys.exit("Error: {}".format(e))

    def run_analyzer(self, analyzerId, dataType, tlp, observable):
        req = self.url + "/api/analyzer/{}/run".format(analyzerId)
        try:
            if dataType == "file":
                file = {
                    "data": (os.path.basename(observable), open(observable, 'rb'), magic.Magic(mime=True).from_file(observable))
                }
                data = {
                    "_json": json.dumps({
                        "dataType": "file",
                        "tlp": tlp
                    })
                }
                return requests.post(req, data=data, files=file, proxies=self.proxies)
            else:
                post = {
                    "data": observable,
                    "attributes": {
                        "dataType": dataType,
                        "tlp": tlp
                    }
                }
                return requests.post(req, headers={'Content-Type': 'application/json'}, data=json.dumps(post), proxies=self.proxies)
        except requests.exceptions.RequestException as e:
            sys.exit("Error: {}".format(e))

    def get_job_report(self, job_id):
        req = self.url + '/api/job/{}/report'.format(job_id)

        try:
            return requests.get(req, proxies=self.proxies)
        except requests.exceptions.RequestException as e:
            sys.exit("Error: {}".format(e))