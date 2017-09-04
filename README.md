[![Join the chat at https://gitter.im/TheHive-Project/TheHive](https://badges.gitter.im/TheHive-Project/TheHive.svg)](https://gitter.im/TheHive-Project/TheHive?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


# Cortex4py
Cortex4py is a Python API client for [Cortex](https://thehive-project.org/), a powerful observable analysis engine where observables such as IP and email addresses, URLs, domain names, files or hashes can be analyzed one by one using a Web interface.

Cortex4py allows analysts to automate these operations and submit observables in bulk mode through the Cortex REST API from alternative SIRP platforms, custom scripts or MISP.

# Caution - WIP
Cortex4py is considered work in progress. It is considered *beta* software though we are using it on a regular basis for the use case outlined above. It should be sufficient in most situations where you need to interact with [Cortex's REST API](https://github.com/CERT-BDF/CortexDocs/blob/master/api/README.md). If not, please feel free to contribute and submit pull requests or [request missing features](https://github.com/CERT-BDF/Cortex4py/issues/new) if you are not comfortable with Python.

# Use It
On macOS and Linux, type:
```
sudo pip install cortex4py
```

Following is an example of a python script that runs an analysis using MaxMind analyzer

```python
import sys
import json
from cortex4py.api import CortexApi
from cortex4py.api import CortexException

api = CortexApi('http://127.0.0.1:9000')

# Run analysis
job_id = None
try:
    response = api.run_analyzer("MaxMind_GeoIP_3_0", "ip", 1, "8.8.8.8")
    job_id = response["id"]
except CortexException as ex:
    print('[ERROR]: Failed to run analyzer: {}'.format(ex.message))
    sys.exit(0)

# Get the job report
try:
    response = api.get_job_report(job_id, '30s')
    print(json.dumps(response, indent=4, sort_keys=True))
except CortexException as ex:
    print('[ERROR]: Failed to get job report'.format(ex.message))
    sys.exit(0)
```

If you are using Python on a Windows operating system, please forgo the `sudo` command.

# License
Cortex4py is an open source and free software released under the [AGPL](https://github.com/CERT-BDF/Cortex4py/blob/master/LICENSE) (Affero General Public License). We, TheHive Project, are committed to ensure that Cortex4py will remain a free and open source project on the long-run.

# Updates
Information, news and updates are regularly posted on [TheHive Project Twitter account](https://twitter.com/thehive_project) and on [the blog](https://blog.thehive-project.org/).

# Contributing
We welcome your contributions. Please feel free to fork the code, play with it, make some patches and send us pull requests using [issues](https://github.com/CERT-BDF/Cortex4py/issues).

We do have a [Code of conduct](code_of_conduct.md). Make sure to check it out before contributing.

# Support
Please [open an issue on GitHub](https://github.com/CERT-BDF/Cortex4py/issues/new) if you'd like to report a bug or request a feature. We are also available on [Gitter](https://gitter.im/TheHive-Project/TheHive) to help you out.

If you need to contact the project team, send an email to <support@thehive-project.org>.

# Community Discussions
We have set up a Google forum at <https://groups.google.com/a/thehive-project.org/d/forum/users>. To request access, you need a Google account. You may create one [using a Gmail address](https://accounts.google.com/SignUp?hl=en) or [without one](https://accounts.google.com/SignUpWithoutGmail?hl=en).

# Website
<https://thehive-project.org/>
