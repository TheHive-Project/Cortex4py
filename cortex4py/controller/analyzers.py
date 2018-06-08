import os
from textwrap import indent

import magic
import json
from typing import List

from cortex4py.query import *
from .abstract import AbstractController
from ..models import Analyzer, Job


class AnalyzersController(AbstractController):
    def __init__(self, api):
        AbstractController.__init__(self, 'analyzer', api)

    def find_all(self, query, **kwargs) -> List[Analyzer]:
        return self._wrap(self._find_all(query, **kwargs), Analyzer)

    def find_one_by(self, query, **kwargs) -> Analyzer:
        return self._wrap(self._find_one_by(query, **kwargs), Analyzer)

    def get_by_id(self, analyzer_id) -> Analyzer:
        return self._wrap(self._get_by_id(analyzer_id), Analyzer)

    def get_by_name(self, name) -> Analyzer:
        return self._wrap(self._find_one_by(Eq('name', name))[0], Analyzer)

    def get_by_type(self, data_type):
        return self._wrap(self._api.do_get('analyzer/type/{}'.format(data_type)).json(), Analyzer)

    def definitions(self):
        return self._wrap

    def enable(self, analyzer_name, config):
        # TODO Not implemented yet
        pass

    def disable(self, analyzer_id):
        return self._api.do_delete('analyzer/{}'.format(analyzer_id))

    def update(self, parameter_list):
        # TODO Not implemented yet
        pass

    def run_by_id(self, analyzer_id, observable, **kwargs):
        tlp = observable.get('tlp', 2)
        data_type = observable.get('dataType', None)

        post = {
            'dataType': data_type,
            'tlp': tlp
        }

        params = {}
        if 'force' in kwargs:
            params['force'] = kwargs.get('force', 1)

        # add additional details
        for key in ['message', 'parameters']:
            if key in observable:
                post[key] = observable.get(key, None)

        if observable.get('dataType') == "file":
            file_path = observable.get('data', None)
            file_def = {
                "data": (os.path.basename(file_path), open(file_path, 'rb'),
                         magic.Magic(mime=True).from_file(file_path))
            }

            data = {
                '_json': json.dumps(post)
            }

            return self._wrap(self._api.do_file_post('analyzer/{}/run'.format(analyzer_id), data,
                                                     files=file_def, params=params).json(), Job)
        else:
            post['data'] = observable.get('data')

            return self._wrap(self._api.do_post('analyzer/{}/run'.format(analyzer_id), post, params).json(), Job)

            # try:
            #     if response.status_code == 200:
            #         return response.json()
            #     elif response.status_code == 400:
            #         self.__handle_error(InvalidInputException(response.text))
            #     else:
            #         self.__handle_error(CortexException(response.text))
            # except Exception as e:
            #     self.__handle_error(e)

    def run_by_name(self, analyzer_name, observable, **kwargs):
        analyzer = self.get_by_name(analyzer_name)

        return self.run_by_id(analyzer.id, observable, **kwargs)
