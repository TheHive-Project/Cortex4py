from .model import Model


class Analyzer(Model):

    def __init__(self, data):
        defaults = {
            'id': None,
            'name': None,
            'analyzerDefinitionId': None,
            'description': None,
            'version': None,
            'author': None,
            'version': None,
            'url': None,
            'license': None,
            'configuration': {}
        }

        if data is None:
            data = dict(defaults)

        self.__dict__ = {k: v for k, v in data.items() if not k.startswith('_')}