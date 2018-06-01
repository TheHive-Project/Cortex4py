from .abstract import AbstractController
from ..models import Organization


class OrganizationsController(AbstractController):
    def __init__(self, api):
        AbstractController.__init__(self, 'organization', api)

    def get_users(self, organization_id, query, **kwargs):
        url = 'organization/{}/user/_search'.format(organization_id)
        params = dict((k, kwargs.get(k, None)) for k in ('sort', 'range'))

        return self._api.do_post(url, {'query': query or {}}, params)

    def create(self, data) -> Organization:

        if isinstance(data, dict):
            data = Organization(data).json()
        elif isinstance(data, Organization):
            data = data.json()

        response = self._api.do_post('organization', data)

        return Organization(response)

    def update(self, org_id, data) -> Organization:
        """
        TODO: Not yet implemented

        curl -XPATCH -H 'Authorization: Bearer **API_KEY**' -H 'Content-Type: application/json' 'http://CORTEX_APP_URL:9001/api/organization/ORG_ID' -d '{
          "description": "New Demo organization",
        }'
        """
        pass

    def delete(self, org_id) -> bool:
        return self._api.do_delete('organization/{}'.format(org_id))
