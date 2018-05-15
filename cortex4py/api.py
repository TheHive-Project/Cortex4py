#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import magic
import requests
from future.utils import raise_from


class InvalidInputException(Exception):
    pass


class CortexException(Exception):
    pass


class CortexApi:
    """
        Python API for Cortex

        :param url: Cortex URL
        :param proxies: dict object defining URLs of http and https proxies
    """

    def __init__(self, url, proxies=None, cert=True, auth=None):
        """
        An client for the REST APIs defined by Cortex

        Args:
            :param url:
            :param proxies (:obj:`dict`, optional): An object defining the http/https proxy URLs.
                Should have two attributes: `http` or `https` indicating the proxy's URL
            :param cert (``str``, optional): True by default to enable cert verification, False to disable it
            :param auth authentication token (required for Cortex-2), can be either a `str` for API key or a `dict`
                with `user` and `password` for basic authentication
        """

        self.url = url
        self.proxies = proxies
        self.cert = cert
        if isinstance(auth, tuple) and len(auth) == 2:
            self.auth = auth
            self.headers = {}
        elif isinstance(auth, str):
            self.auth = None
            self.headers = {"Authorization": "Bearer %s" % auth}
        else:
            self.auth = None
            self.headers = None

    def __handle_error(self, exception):
        if isinstance(exception, CortexException):
            raise exception

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
            response = requests.get(req, proxies=self.proxies, verify=self.cert, auth=self.auth, headers=self.headers)

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
                response = requests.post(req,
                                         data=data,
                                         files=file_def,
                                         proxies=self.proxies,
                                         verify=self.cert,
                                         auth=self.auth,
                                         headers=self.headers)

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
                headers = {'Content-Type': 'application/json'}
                headers.update(self.headers)
                response = requests.post(req,
                                         headers=headers,
                                         data=json.dumps(post),
                                         proxies=self.proxies,
                                         verify=self.cert,
                                         auth=self.auth)

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
            response = requests.get(req, proxies=self.proxies, verify=self.cert, auth=self.auth, headers=self.headers)

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
            response = requests.delete(req,
                                       proxies=self.proxies,
                                       verify=self.cert,
                                       auth=self.auth,
                                       headers=self.headers)

            if response.status_code == 200:
                return True
            else:
                self.__handle_error(CortexException(response.text))
        except requests.exceptions.RequestException as e:
            self.__handle_error(e)

    def create_organization(self, name, description='', status='Active'):
        url = self.url + '/api/organization'
        data = {
            'name': name,
            'description': description,
            'status': status,
        }

        try:
            res = requests.post(url, json=data, headers=self.headers)
        except requests.exceptions.RequestException as e:
            self.__handle_error(e)
        else:
            if res.status_code == 201:
                return res.json()
            self.__handle_error(CortexException(res.text))

    def create_user(self, login, name, organization, roles={0: 'read', 1: 'analyze'}):
        url = self.url + '/api/user'
        data = {
            'login': login,
            'name': name,
            'organization': organization,
            'roles': roles
        }

        try:
            res = requests.post(url, json=data, headers=self.headers)
        except requests.exceptions.RequestException as e:
            self.__handle_error(e)
        else:
            if res.status_code == 201:
                return res.json()
            self.__handle_error(CortexException(res.text))

    def set_user_password(self, login, password):
        url = self.url + '/api/user/{}/password/set'.format(login)
        data = {'password': password}

        try:
            res = requests.post(url, json=data, headers=self.headers)
        except requests.exceptions.RequestException as e:
            self.__handle_error(e)
        else:
            if res.status_code == 204:
                return res.json()
            self.__handle_error(CortexException(res.text))

    def renew_api_key(self, login):
        url = self.url + '/api/user/{}/key/renew'.format(login)

        try:
            res = requests.post(url, headers=self.headers)
        except requests.exceptions.RequestException as e:
            self.__handle_error(e)
        else:
            if res.status_code == 200:
                #Cortex returns a raw string here, not a json object.
                return res.text
            self.__handle_error(CortexException(res.text))

    def add_analyzer(self, analyzer_name, cache_duration=None, check_tlp=True, max_tlp=2, **kwargs):
        url = self.url + '/api/organization/analyzer/' + analyzer_name
        data = {
            'jobCache': cache_duration,
            'name': analyzer_name,
            'configuration': {
                'check_tlp': check_tlp,
                'max_tlp': max_tlp,
                **kwargs
            }
        }

        try:
            res = requests.post(url, json=data, headers=self.headers)
        except requests.exceptions.RequestException as e:
            self.__handle_error(e)
        else:
            if res.status_code == 201:
                return res.json()
            self.__handle_error(res.text)

    def remove_analyzer(self, analyzer_id):
        url = self.url + '/api/analyzer/{}'.format(analyzer_id)

        try:
            res = requests.delete(url, headers=self.headers)
        except requests.exceptions.RequestException as e:
            self.__handle_error(e)
        else:
            if res.status_code != 204:
                self.__handle_error(CortexException(res.text))

    def update_analyzer(self, analyzer_id, cache_duration=None, check_tlp=True, max_tlp=2, **kwargs):
        url = self.url + '/api/analyzer/{}'.format(analyzer_id)
        data = {
            'jobCache': cache_duration,
            'configuration': {
                'check_tlp': check_tlp,
                'max_tlp': max_tlp,
                **kwargs
            }
        }

        try:
            res = requests.patch(url, json=data, headers=self.headers)
        except requests.exceptions.RequestException as e:
            self.__handle_error(e)
        else:
            if res.status_code == 200:
                return res.json()
            self.__handle_error(res.text)

