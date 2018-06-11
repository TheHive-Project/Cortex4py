#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import requests
import warnings

from .exceptions import *
from .controller.organizations import OrganizationsController
from .controller.users import UsersController
from .controller.jobs import JobsController
from .controller.analyzers import AnalyzersController


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
    def __recover(exception):
        print("[ERROR]: {0}".format(exception))
        if isinstance(exception, requests.exceptions.HTTPError):
            if exception.response.status_code == 404:
                raise CortexException("Resource not found") from exception
            elif exception.response.status_code == 401:
                raise CortexException("Authentication error") from exception
            elif exception.response.status_code == 403:
                raise CortexException("Authorization error") from exception
            else:
                raise CortexException("Invalid input exception") from exception
        elif isinstance(exception, requests.exceptions.ConnectionError):
            raise CortexException("Cortex service is unavailable") from exception
        elif isinstance(exception, requests.exceptions.RequestException):
            raise CortexException("Cortex request exception") from exception
        else:
            raise CortexException("Unexpected exception") from exception

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

            response.raise_for_status()
            return response
        except Exception as ex:
            self.__recover(ex)

    def do_file_post(self, endpoint, data, **kwargs):
        headers = {
            'Authorization': 'Bearer {}'.format(self.__api_key)
        }

        try:
            response = requests.post('{}{}'.format(self.__base_url, endpoint),
                                     headers=headers,
                                     proxies=self.__proxies,
                                     data=data,
                                     verify=self.__verify_cert,
                                     **kwargs)
            response.raise_for_status()
            return response
        except Exception as ex:
            self.__recover(ex)

    def do_post(self, endpoint, data, params={}, **kwargs):
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
                                     verify=self.__verify_cert,
                                     **kwargs)
            response.raise_for_status()
            return response
        except Exception as ex:
            self.__recover(ex)

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
            response.raise_for_status()
            return response
        except Exception as ex:
            self.__recover(ex)

    def do_delete(self, endpoint):
        headers = {
            'Authorization': 'Bearer {}'.format(self.__api_key)
        }

        try:
            response = requests.delete('{}{}'.format(self.__base_url, endpoint),
                                       headers=headers,
                                       proxies=self.__proxies,
                                       verify=self.__verify_cert)
            response.raise_for_status()
            return True
        except Exception as ex:
            self.__recover(ex)
        pass

    def status(self):
        return self.do_get('status')

    """
    Method for backward compatibility 
    """
    def get_analyzers(self, data_type=None):
        if data_type is not None:
            return self.analyzers.find_all()
        else:
            return self.analyzers.get_by_type(data_type)

    def run_analyzer(self, analyzer_id, data_type, tlp, observable):
        options = {
            'data': observable,
            'tlp': tlp,
            'dataType': data_type
        }
        return self.analyzers.run_by_name(analyzer_id, options)

    def get_job_report(self, job_id, timeout='Inf'):        
        return self.jobs.get_report_async(job_id, timeout)        

    def delete_job(self, job_id):        
        return self.jobs.delete(job_id)

