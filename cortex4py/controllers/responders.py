from typing import List

from cortex4py.query import *
from .abstract import AbstractController
from ..models import Responder, Job, ResponderDefinition


class RespondersController(AbstractController):
    def __init__(self, api):
        AbstractController.__init__(self, 'responder', api)

    def find_all(self, query, **kwargs) -> List[Responder]:
        return self._wrap(self._find_all(query, **kwargs), Responder)

    def find_one_by(self, query, **kwargs) -> Responder:
        return self._wrap(self._find_one_by(query, **kwargs), Responder)

    def get_by_id(self, worker_id) -> Responder:
        return self._wrap(self._get_by_id(worker_id), Responder)

    def get_by_name(self, name) -> Responder:
        return self._wrap(self._find_one_by(Eq('name', name)), Responder)

    def get_by_type(self, data_type) -> List[Responder]:
        return self._wrap(self._api.do_get('responder/type/{}'.format(data_type)).json(), Responder)

    def definitions(self) -> List[ResponderDefinition]:
        return self._wrap(self._api.do_get('responderdefinition').json(), ResponderDefinition)

    def enable(self, responder_name, config) -> Responder:
        url = 'organization/responder/{}'.format(responder_name)
        config['name'] = responder_name

        return self._wrap(self._api.do_post(url, config).json(), Responder)

    def update(self, worker_id, config) -> Responder:
        url = 'responder/{}'.format(worker_id)
        config.pop('name', None)

        return self._wrap(self._api.do_patch(url, config).json(), Responder)

    def disable(self, worker_id) -> bool:
        return self._api.do_delete('responder/{}'.format(worker_id))

    def run_by_id(self, worker_id, data, **kwargs) -> Job:
        tlp = data.get('tlp', 2)
        data_type = data.get('dataType', None)

        post = {
            'dataType': data_type,
            'tlp': tlp
        }

        # add additional details
        for key in ['message', 'parameters']:
            if key in data:
                post[key] = data.get(key, None)

        post['data'] = data.get('data')

        return self._wrap(self._api.do_post('responder/{}/run'.format(worker_id), post).json(), Job)

    def run_by_name(self, responder_name, data, **kwargs) -> Job:
        responder = self.get_by_name(responder_name)

        return self.run_by_id(responder.id, data, **kwargs)
