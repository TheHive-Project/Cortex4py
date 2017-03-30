#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import os
import magic
import requests


class CortexApi:
    """
        Python API for Cortex

        :param url: Cortex URL
        :param proxies: dict object defining URLs of http and https proxies
    """

    def __init__(self, url, proxies):
        """
        An client for the REST APIs defined by Cortex

        Args:
            :param url:
            :param proxies (:obj:`dict`, optional): An object defining the http/https proxy URLs.
                Should have two attributes: `http` or `https` indicating the proxy's URL
        """

        self.url = url
        self.proxies = proxies

    def get_analyzers(self, data_type=None):
        """
            Get the list of all analyzers or the analyzers that can run on the observables of type `data_type`

            :param data_type: Observable data type
            :type data_type: ``str``

            :return: HTTP Request response object, where the body is a JSON array of analyzer objects
        """
        if data_type is not None:
            req = self.url + '/api/analyzer/type/{}'.format(str(data_type))
        else:
            req = self.url + '/api/analyzer'

        try:
            return requests.get(req, proxies=self.proxies)
        except requests.exceptions.RequestException as e:
            sys.exit("Error: {}".format(e))

    def run_analyzer(self, analyzer_id, data_type, tlp, observable):
        """
            Call the REST API responsible of running a given analyzer on a given observable

            :param analyzer_id: The identifier of the analyzer
            :param data_type: The observable's data type
            :param tlp: The observable's TLP
            :param observable: The observable value or the file path if the observable is a File

            :type analyzer_id: ``str``
            :type data_type: ``str``
            :param tlp: The observable's TLP
            :param observable: The observable value or the file path if the observable is a File

            :return: HTTP Request response object, where the body is a JSON object describing a job
        """
        req = self.url + "/api/analyzer/{}/run".format(analyzer_id)
        try:
            if data_type == "file":
                file = {
                    "data": (os.path.basename(observable), open(observable, 'rb'),
                             magic.Magic(mime=True).from_file(observable))
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
                        "dataType": data_type,
                        "tlp": tlp
                    }
                }
                return requests.post(req,
                                     headers={'Content-Type': 'application/json'},
                                     data=json.dumps(post),
                                     proxies=self.proxies)
        except requests.exceptions.RequestException as e:
            sys.exit("Error: {}".format(e))

    def get_job_report(self, job_id):
        """
            Call the REST API returning the report of a job identified by the given `job_id`

            :param job_id: The job's identifier
            :type job_id: ``str``

            :return: HTTP Request response object, where the body is a JSON object describing a job
        """
        req = self.url + '/api/job/{}/report'.format(job_id)

        try:
            return requests.get(req, proxies=self.proxies)
        except requests.exceptions.RequestException as e:
            sys.exit("Error: {}".format(e))
