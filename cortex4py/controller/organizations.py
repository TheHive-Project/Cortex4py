from .abstract import AbstractController


class OrganizationsController(AbstractController):
    def __init__(self, api):
        AbstractController.__init__(self, 'organization', api)

    def get_users(self, organization_id, query, **kwargs):
        url = 'organization/{}/users'.format(organization_id)
        params = dict((k, kwargs.get(k, None)) for k in ('sort', 'range'))

        return self._api.do_post(url, {'query': query or {}}, params)
