from .abstract import AbstractController


class JobsController(AbstractController):
    def __init__(self, api):
        AbstractController.__init__(self, 'job', api)

    def get_report(self, job_id):
        return self._api.do_get('job/{}/report'.format(job_id)).json()

    def get_report_async(self, job_id, timeout='Inf'):
        return self._api.do_get('job/{}/waitreport?atMost={}'.format(job_id, timeout)).json()

    def get_artifacts(self, job_id):
        return self._api.do_get('job/{}/artifacts'.format(job_id)).json()

    def delete(self, job_id):
        return self._api.do_delete('job/{}'.format(job_id))