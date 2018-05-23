from .abstract import AbstractController


class AnalyzersController(AbstractController):
    def __init__(self, api):
        AbstractController.__init__(self, 'analyzer', api)
