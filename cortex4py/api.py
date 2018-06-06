#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import warnings

from .exceptions import *
from .controller.organizations import OrganizationsController
from .controller.users import UsersController
from .controller.jobs import JobsController
from .controller.analyzers import AnalyzersController


import json
import os
import magic
import requests
from future.utils import raise_from


class Api(object):
    """This is the main class for communicating with the Cortex API. As this is a new major version, authentication is
    only possible through the api key. Basic auth with user/pass is deprecated."""
    def __init__(self, url, api_key, **kwargs):
        if not isinstance(url, str) or not isinstance(api_key, str):
            raise TypeError('URL and API key are required and must be of type string.')

        # Drop a warning for python2 because reasons
        if int(sys.version[0]) < 3:
            warnings.warn('You are using Python 2.x. That can work, but is not supported.')

        self.__api_key = api_key
        self.__url = url
        self.__base_url = '{}/api/'.format(url)
        self.__proxies = kwargs.get('proxies', {})
        self.__verify_cert = kwargs.get('verify_cert', kwargs.get('cert', True))

        self.organizations = OrganizationsController(self)
        self.users = UsersController(self)
        self.jobs = JobsController(self)
        self.analyzers = AnalyzersController(self)

    @staticmethod
    def __recover(ex):
        """
        TODO catch the following exceptions
        - requests.exceptions.RequestException
        - requests.exceptions.RequestException
        - requests.exceptions.RequestException
        - requests.exceptions.RequestException
        - requests.exceptions.RequestException
        - requests.exceptions.RequestException
        """
        print("[ERROR]: {0}".format(ex))
        pass

    def do_get(self, endpoint, params={}):
        headers = {
            'Authorization': 'Bearer {}'.format(self.__api_key)
        }

        try:
            response = requests.get('{}{}'.format(self.__base_url, endpoint),
                                    headers=headers,
                                    params=params,
                                    proxies=self.__proxies,
                                    verify=self.__verify_cert)

            return response
        except Exception as ex:
            return self.__recover(ex)

    def do_post(self, endpoint, data, params={}):
        headers = {
            'Authorization': 'Bearer {}'.format(self.__api_key),
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post('{}{}'.format(self.__base_url, endpoint),
                                     headers=headers,
                                     proxies=self.__proxies,
                                     json=data,
                                     params=params,
                                     verify=self.__verify_cert)

            return response
        except Exception as ex:
            return self.__recover(ex)

    def do_patch(self, endpoint, data, params={}):
        headers = {
            'Authorization': 'Bearer {}'.format(self.__api_key),
            'Content-Type': 'application/json'
        }

        try:
            response = requests.patch('{}{}'.format(self.__base_url, endpoint),
                                      headers=headers,
                                      proxies=self.__proxies,
                                      json=data,
                                      params=params,
                                      verify=self.__verify_cert)

            return response
        except Exception as ex:
            return self.__recover(ex)

    def do_delete(self, endpoint):
        headers = {
            'Authorization': 'Bearer {}'.format(self.__api_key)
        }

        try:
            requests.delete('{}{}'.format(self.__base_url, endpoint),
                            headers=headers,
                            proxies=self.__proxies,
                            verify=self.__verify_cert)

            return True
        except Exception as ex:
            return self.__recover(ex)
        pass

    def status(self):
        return self.do_get('status')

    def get_analyzers(self, data_type=None):
        # TODO Not implemented yet
        pass

    def run_analyzer(self, analyzer_id, data_type, tlp, observable):
        # TODO Not implemented yet
        pass

    def get_job_report(self, job_id, timeout='Inf'):        
        return self.jobs.get_report_async(job_id, timeout)        

    def delete_job(self, job_id):        
        return self.jobs.delete(job_id)


class CortexApi:
    """
        Python API for Cortex

        :param url: Cortex URL
        :param proxies: dict object defining URLs of http and https proxies
    """

    def __init__(self, url, proxies={}, cert=True):
        """
        An client for the REST APIs defined by Cortex

        Args:
            :param url:
            :param proxies (:obj:`dict`, optional): An object defining the http/https proxy URLs.
                Should have two attributes: `http` or `https` indicating the proxy's URL
            :param cert (``str``, optional): True by default to enable cert verification, False to disable it
                    
        """

        self.url = url
        self.proxies = proxies
        self.cert = cert

    def __handle_error(self, exception):
        if isinstance(exception, requests.exceptions.ConnectionError):
            raise_from(CortexException("Cortex service is unavailable"), exception)
        elif isinstance(exception, requests.exceptions.RequestException):
            raise_from(CortexException("Cortex request exception"), exception)
        elif isinstance(exception, InvalidInputException):
            raise_from(CortexException("Invalid input exception"), exception)
        else:
            raise_from(CortexException("Unexpected exception"), exception)

    def get_analyzers(self, data_type=None):
        """
            Get the list of all analyzers or the analyzers that can run on the observables of type `data_type`

            :param data_type: Observable data type
            :type data_type: ``str``

            :return: A JSON array of analyzer objects
        """
        if data_type is not None:
            req = self.url + '/api/analyzer/type/{}'.format(str(data_type))
        else:
            req = self.url + '/api/analyzer'

        try:
            response = requests.get(req, proxies=self.proxies, verify=self.cert)

            if response.status_code == 200:
                return response.json()
            else:
                self.__handle_error(CortexException(response.text))
        except Exception as e:
            self.__handle_error(e)

    def run_analyzer(self, analyzer_id, data_type, tlp, observable):
        """
            Call the REST API responsible of running a given analyzer on a given observable

            :param analyzer_id: The identifier of the analyzer
            :param data_type: The observable's data type
            :param tlp: The observable's TLP
            :param observable: The observable value or the file path if the observable is a File

            :type analyzer_id: ``str``
            :type data_type: ``str``
            :type tlp: ``integer`` 
            :type observable: ``str`` 

            :return: A JSON object describing a job
        """
        req = self.url + "/api/analyzer/{}/run".format(analyzer_id)

        if data_type == "file":
            file_def = {
                "data": (os.path.basename(observable), open(observable, 'rb'),
                         magic.Magic(mime=True).from_file(observable))
            }
            data = {
                "_json": json.dumps({
                    "dataType": "file",
                    "tlp": tlp
                })
            }
            try:
                response = requests.post(req, data=data, files=file_def, proxies=self.proxies, verify=self.cert)

                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 400:
                    self.__handle_error(InvalidInputException(response.text))
                else:
                    self.__handle_error(CortexException(response.text))
            except Exception as e:
                self.__handle_error(e)

        else:
            post = {
                "data": observable,
                "attributes": {
                    "dataType": data_type,
                    "tlp": tlp
                }
            }
            try:
                response = requests.post(req,
                                         headers={'Content-Type': 'application/json'},
                                         data=json.dumps(post),
                                         proxies=self.proxies,
                                         verify=self.cert)

                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 400:
                    self.__handle_error(InvalidInputException(response.text))
                else:
                    self.__handle_error(CortexException(response.text))
            except Exception as e:
                self.__handle_error(e)

    def get_job_report(self, job_id, timeout='Inf'):
        """
            Call the REST API returning the report of a job identified by the given `job_id`

            :param job_id: The job's identifier
            :param timeout: The wait duration using the format 30s, 10m, 1h 
            
            :type job_id: ``str``
            :type timeout: ``str``

            :return: A JSON object describing a job report
        """
        req = self.url + '/api/job/{}/waitreport?atMost={}'.format(job_id, timeout)

        try:
            response = requests.get(req, proxies=self.proxies, verify=self.cert)

            if response.status_code == 200:
                return response.json()
            else:
                self.__handle_error(CortexException(response.text))
        except requests.exceptions.RequestException as e:
            self.__handle_error(e)

    def delete_job(self, job_id):
        """
            Call the REST API that deletes the job identified by the given `job_id`

            :param job_id: The job's identifier
         
            :type job_id: ``str``         

            :return: True if the deletion completes successfully
        """
        req = self.url + '/api/job/{}'.format(job_id)
        try:
            response = requests.delete(req, proxies=self.proxies, verify=self.cert)

            if response.status_code == 200:
                return True
            else:
                self.__handle_error(CortexException(response.text))
        except requests.exceptions.RequestException as e:
            self.__handle_error(e)
