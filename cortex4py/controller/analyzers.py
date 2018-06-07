from .abstract import AbstractController


class AnalyzersController(AbstractController):
    def __init__(self, api):
        AbstractController.__init__(self, 'analyzer', api)

    def enable(self, analyzer_name, config):       
        # TODO Not implemented yet
        pass

    def disable(self, analyzer_id):
        return self._api.do_delete('analyzer/{}'.format(analyzer_id))

    def get_for_type(self, data_type):
        return self._api.do_get('analyzer/type/{}'.format(data_type)).json()

    def update(self, parameter_list):
        # TODO Not implemented yet
        pass

    def run(self, options):
        # TODO Not implemented yet
        pass