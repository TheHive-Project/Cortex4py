from .abstract import AbstractController


class JobsController(AbstractController):
    def __init__(self, api):
        AbstractController.__init__(self, 'job', api)
