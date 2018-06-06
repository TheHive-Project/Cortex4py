from .abstract import AbstractController


class JobsController(AbstractController):
    def __init__(self, api):
        AbstractController.__init__(self, 'job', api)

    def get_report(self, job_id):
        return self._api.do_get('job/{}/report'.format(job_id)).json()

    def get_report_async(self, job_id, duration='Inf'):
        return self._api.do_get('job/{}/waitreport?atMost={}'.format(job_id, duration)).json()

    def get_artifacts(self, job_id):
        return self._api.do_get('job/{}/artifacts'.format(job_id)).json()

    def revoke_key(self, job_id):
        return self._api.do_delete('job/{}'.format(job_id))