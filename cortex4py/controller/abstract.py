class AbstractController(object):
    def __init__(self, endpoint, api):
        self._api = api
        self._endpoint = endpoint

    def _wrap(self, data, cls):
        if isinstance(data, dict):
            return cls(data)
        elif isinstance(data, list):
            return list(map(lambda item: cls(item), data))
        else:
            return data

    def _find_all(self, query, **kwargs):
        url = '{}/_search'.format(self._endpoint)
        params = dict((k, kwargs.get(k, None)) for k in ('sort', 'range'))

        return self._api.do_post(url, {'query': query or {}}, params).json()

    def _find_one_by(self, query, **kwargs):
        url = '{}/_search'.format(self._endpoint)

        params = {
            'range': '0-1'
        }
        if 'sort' in kwargs:
            params['sort'] = kwargs['sort']

        return self._api.do_post(url, {'query': query or {}}, params).json()

    def _count(self, query):
        url = '{}/_stats'.format(self._endpoint)

        payload = {
            'query': query or {},
            'stats': [{
                '_agg': 'count'
            }]
        }

        response = self._api.do_post(url, payload, {}).json()

        if response is not None:
            return response.get('count', None)
        else:
            return None

    def _get_by_id(self, obj_id):
        url = '{}/{}'.format(self._endpoint, obj_id)

        return self._api.do_get(url).json()

    def update_one_by_id(self, obj_id, **attributes):
        pass

    def update_one_by_object(self, updated_obj, limit_attributes=None):
        pass
