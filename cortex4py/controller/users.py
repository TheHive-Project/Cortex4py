from .abstract import AbstractController
from ..models import User


class UsersController(AbstractController):
    def __init__(self, api):
        AbstractController.__init__(self, 'user', api)

    def create(self, data) -> User:

        if isinstance(data, dict):
            data = User(data).json()
        elif isinstance(data, User):
            data = data.json()

        response = self._api.do_post('user', data).json()

        return User(response)

    def update(self):
        # TODO Not yet implemented
        pass

    def delete(self, user_id):
        return self._api.do_patch('user/{}'.format(user_id), {
            'status': 'Locked'
        }).json()

    def set_password(self, user_id, password):
        return self._api.do_post('user/{}/password/set'.format(user_id), {'password': password}).text

    def change_password(self, user_id, current_password, new_password ):
        return self._api.do_post('user/{}/password/change'.format(user_id), {
            'currentPassword': current_password,
            'password': new_password
        }).text

    def set_key(self, user_id):
        return self._api.do_post('user/{}/key/renew'.format(user_id), {}).text

    def renew_key(self, user_id):
        return self.set_key(user_id)

    def get_key(self, user_id):
        return self._api.do_get('user/{}/key'.format(user_id)).text

    def revoke_key(self, user_id):
        return self._api.do_delete('user/{}/key'.format(user_id))