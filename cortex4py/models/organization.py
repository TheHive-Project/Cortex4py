import json


class Organization(object):

    def __init__(self, data):
        self.__dict__ = {k: v for k, v in data.items() if not k.startswith('_')}

    def __str__(self):
        return json.dumps(self.__dict__, indent=2)

    def json(self):
        return self.__dict__
