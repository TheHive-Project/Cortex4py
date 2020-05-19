import os

import magic
import json
from typing import List

from cortex4py.query import *
from .abstract import AbstractController
from ..models import Analyzer, Job, AnalyzerDefinition


class RespondersController(AbstractController):
    def __init__(self, api):
        AbstractController.__init__(self, 'responder', api)

    def find_all(self, query, **kwargs) -> List[Analyzer]:
        return self._wrap(self._find_all(query, **kwargs), Analyzer)

    def find_one_by(self, query, **kwargs) -> Analyzer:
        return self._wrap(self._find_one_by(query, **kwargs), Analyzer)

    def get_by_id(self, responder_id) -> Analyzer:
        return self._wrap(self._get_by_id(responder_id), Analyzer)

    def get_by_name(self, name) -> Analyzer:
        return self._wrap(self._find_one_by(Eq('name', name)), Analyzer)

    def get_by_type(self, data_type) -> List[Analyzer]:
        return self._wrap(self._api.do_get('responder/type/{}'.format(data_type)).json(), Analyzer)

    def definitions(self) -> List[AnalyzerDefinition]:
        return self._wrap(self._api.do_get('analyzerdefinition').json(), AnalyzerDefinition)

    def enable(self, responder_name, config) -> Analyzer:
        url = 'organization/responder/{}'.format(responder_name)
        config['name'] = responder_name

        return self._wrap(self._api.do_post(url, config).json(), Analyzer)

    def update(self, responder_id, config) -> Analyzer:
        url = 'responder/{}'.format(responder_id)
        config.pop('name', None)

        return self._wrap(self._api.do_patch(url, config).json(), Analyzer)

    def disable(self, responder_id) -> bool:
        return self._api.do_delete('responder/{}'.format(responder_id))

    def run_by_id(self, responder_id, observable, **kwargs) -> Job:
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

            return self._wrap(self._api.do_file_post('responder/{}/run'.format(responder_id), data,
                                                     files=file_def, params=params).json(), Job)
        else:
            post['data'] = observable.get('data')

            return self._wrap(self._api.do_post('responder/{}/run'.format(responder_id), post, params).json(), Job)

    def run_by_name(self, responder_name, observable, **kwargs) -> Job:
        responder = self.get_by_name(responder_name)

        return self.run_by_id(responder.id, observable, **kwargs)
