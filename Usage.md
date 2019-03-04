# How to Use Cortex4py

This document is a usage guide of the Cortex4py library for writing custom scripts that interact with the [Cortex 2](https://github.com/TheHive-Project/Cortex) APIs.

Cortex4py 2 requires Python 3. It does not work with Cortex 1.x.

## Table of Contents

* [Introduction](#introduction)
  * [Library architecture](#library-architecture)
  * [Migration](#migration)
  * [Proxy and certificate verification](#proxy-and-certificate-verification)
  * [Backward compatibility](#backward-compatibility)
  * [Exception handling](#exception-handling)
* [Organization operations](#organization-operations)
  * [Model](#model)
  * [Methods](#methods)
  * [Examples](#examples)
* [User operations](#user-operations)
  * [Model](#model-1)
  * [Methods](#methods-1)
  * [Examples](#examples-1)
* [Analyzer operations](#analyzer-operations)
  * [Model](#model-2)
  * [Methods](#methods-2)
  * [Examples](#examples-2)
* [Job operations](#job-operations)
  * [Model](#model-3)
  * [Methods](#methods-3)
  * [Examples](#examples-3)

## Introduction

Cortex4py 2 is a new version of the library, that is only compatible with Cortex 2.x. It supports authentication and covers almost all the [available APIs]([https://github.com/TheHive-Project/CortexDocs/blob/master/api/api-guide.md), including administration calls.

### Library Architecture

Cortex4py 2 has the following structure:

```plain
├── cortex4py
│   ├── api
│   ├── controllers
│   │   ├── abstract
│   │   ├── analyzers
│   │   ├── jobs
│   │   ├── organizations
│   │   └── users
│   ├── exceptions
│   ├── models
│   │   ├── analyzer
│   │   ├── analyzer_definition
│   │   ├── job
│   │   ├── job_artifact
│   │   ├── model
│   │   ├── organization
│   │   └── user
│   └── query
```

- The **model** classes represent the data objects and extend the `cortex4py.models.Model` that provides `json()` methods returning a JSON `dict` from every model object.
- The **controllers** classes wrap the available methods that call Cortex APIs.
- The **api** class is the main class giving access to the different controllers.
- **query.*** are utility methods that allow building search queries.
- **exceptions.*** are supported exceptions

### Migration
If you have already written scripts using `cortex4py` 1.x (for Cortex 1), we tried to keep the already available methods. However, we recommend you adapt your code to leverage the new `cortex4py` 2 classes and methods as soon as feasible. Moreover, the existing scripts must be updated to support authentication if you intend to use them with Cortex 2.

To instantiate a Cortex 1 API object, developers used to write the following code:

````python
from cortex4py.api import CortexApi

api = CortexApi('http://CORTEX_APP_URL.1:9000')
````

This code must be replaced with something like the example below for Cortex 2:

```python
from cortex4py.api import Api

api = Api('http://CORTEX_APP_URL:9001', '**API_KEY**')
```

### Proxy and Certificate Verification
Cortex4py 2 allows specifying a proxy configuration should your program requires one. The library also adds an option to enable or disable certificate verification.

```python
from cortex4py.api import Api

api = Api('http://CORTEX_APP_URL:9001', '**API_KEY**', proxies={
    'http': 'http://PROXY_URL:PROXY_PORT',
    'https': 'http://PROXY_URL:PROXY_PORT'
}, verify_cert=False)
```

`verify_cert` can be:

- `True`
- `False`
- String representing the path to the certificate file.

**Note**: `verify_cert` replaces the Cortex4py 1 `cert` argument which has been deprecated.

### Backward Compatibility

Cortex4py 2 implements the methods that were available in the old version of the library:

```python
from cortex4py.api import Api

api = Api('http://CORTEX_APP_URL:9001', '**API_KEY**')

analyzers = api.get_analyzers('ip')
job = api.run_analyzer('Abuse_Finder_2_0', 'domain', 2, 'google.com')
job_with_report = api.get_job_report('XXXXXX', timeout='Inf')        
job_deleted = api.delete_job('XXXXXX')
```

**Note**: These methods are now deprecated.

### Exception Handling

All the operations supported by the library can raise errors that inherit a `cortex4py.exceptions.CortexException` exception class. 

Possible errors are listed below:

| Error Exception | Error message | Description |
| --------- | --------- | ----------- |
| `cortex.exceptions.NotFoundError` | `Resource not found` | A 404 error occurred |
| `cortex.exceptions.AuthenticationError` | `Authentication error` | A 401 error occurred |
| `cortex.exceptions.AuthorizationError` | `Authorization error` | A 403 error occurred |
| `cortex.exceptions.InvalidInputError` | `Invalid input exception` | A 400 error occurred |
| `cortex.exceptions.ServiceUnavailableError` | `Cortex service is unavailable` | Connection issue. Cortex is not available |
| `cortex.exceptions.ServerError` | `Cortex request exception` | A 500 error occurred |
| `cortex.exceptions.CortexError` | `Unexpected exception` | An unhandled error occurred |

## Organization Operations

The `OrganizationController` class provides a set of methods to deal with Cortex organizations.

### Model

An organization is represented by the following model class:

| Field | Description | Type |
| --------- | ----------- | ---- |
|`id`| Organization's identifier | readonly |
|`name`| Organization's name, can be specified during creation only. | readonly |
|`description`| Organization's description | writable |
|`status`| Organization's status, `Active` or `Locked`| writable |
|`createdAt` | Creation date | computed |
|`createdBy` | User who created the org | computed |
|`updatedAt` | Last update | computed |
|`updatedBy` | User who last updated the org | computed |

### Methods

| Method | Description | Return type |
| --------- | ----------- | ---- |
|`count(query)` | Requires `superadmin` role, Returns the number of organizations corresponding to the `query` | Number |
|`find_all(query,**kwargs)` | Requires `superadmin` role, returns a list of `Organization` objects, based on `query`, `range` and `sort` parameters | List[Organization] |
|`find_one_by(query,**kwargs)` | Requires `superadmin` role, returns the first `Organization` object, based on `query` and `sort` parameters | Organization |
|`get_by_id(org_id)` | Requires `orgadmin` or `superadmin` roles, returns an `Organization` by its `id` | Organization |
|`get_users(org_id,query,**kwargs)` | Requires `orgadmin` role, returns the list of `User` objects remaining to the `Organization` identified by `org_id` | List[User] |
|`get_analyzers()` | Requires `orgadmin` role, returns the list of enabled `Analyzer` objects remaining to the `Organization` of the current user | List[Analyzer]|
|`create(data)` | Requires `superadmin` role, returns the create `Organization` object. `data` could be a JSON or `Organization` objects | Organization |
|`update(org_id,data,fields)` | Requires `superadmin` role, returns the updated `Organization` object. `data` can be a JSON or `Organization` object. `fields` parameter is an array of field names to update | Organization |
|`delete(org_id)` | Requires `superadmin` role, returns `true` if the delete completes successfully | Boolean |

### Examples

The following example shows how to manipulate organizations as a `superadmin` user:

```python
from cortex4py.api import Api
from cortex4py.query import *
from cortex4py.models import Organization

api = Api('http://CORTEX_APP_URL:9001', '**API_KEY**')

# Find how many locked organizations exist
count = api.organizations.count(Eq('status', 'Locked'))

# Fetch the last 10 created organizations
locked_orgs = api.organizations.find_all({}, range='0-10', sort='-createdAt')

# Display the name of the locked organizations
for org in locked_orgs:
  print('Organization {} is {}'.format(org.name, org.status))

# Create a new organization
new_org = api.organizations.create(Organization({
    "name": "demo",
    "description": "This is a demo organization",
    "status": "Active"
}))

# Display its id
print(new_org.id)

# Update the newly created org
new_org = api.organizations.update(new_org.id, {
  'description': 'This is an disabled organization'
})

# Delete the newly created org
api.organizations.delete(new_org.id)
```

The following example shows how to manipulate organizations as a `orgadmin` user:

```python
import json

from cortex4py.api import Api
from cortex4py.query import *

api = Api('http://CORTEX_APP_URL:9001', '**API_KEY**')

# Get details of an organization
org = api.organizations.get_by_id('demo')

# Print the json representation of the Organization object
print(json.dumps(org.json(), indent=2))

# Fetch the last 5 created and active users
users = api.organizations.get_users(org.id, Eq('status', 'Active'), range='0-5', sort='-createdAt')

# Display the usernames
for user in users:
  print('User {} has roles {}'.format(user.name, user.roles))

# Fetch the organization analyzers
for a in api.organizations.get_analyzers():
  print(a.name)
```

## User Operations

The `UserController` class provides a set of methods to handle users.

### Model

A user is represented by the following model class:

| Field | Description | Type |
| --------- | ----------- | ---- |
|`id`| Users's identifier | readonly |
|`login`| User's login, can be specified during creation only. | readonly |
|`name`| User's full name | writable |
|`organization`| Users's organization. Can be specified during the creation of the user, or updated only by `superadmin` users | writable |
|`status`| User's status, `Ok` or `Locked`| writable |
|`createdAt` | Creation date | computed |
|`createdBy` | User who created the org | computed |
|`updatedAt` | Last update | computed |
|`updatedBy` | User who last updated the org | computed |
|`hasKey` | true when the user has an API key | computed |
|`hasPassword` | true if the user has a password | computed |

### Methods

| Method | Description | Return type |
| --------- | ----------- | ---- |
|`find_all(query,**kwargs)` | Returns a list of `User` objects, based on `query`, `range` and `sort` parameters | List[User] |
|`find_one_by(query,**kwargs)` | Returns the first `User` object, based on `query` and `sort` parameters | User |
|`get_by_id(user_id)` | Returns a `User` by its `user_id` | User |
|`create(data)` | Returns the create `User` object. `data` could be a JSON or `User` objects | User |
|`update(user_id,data,fields)` | Returns the updated `User` object. `data` can be a JSON or `User` object. `fields` parameter is an array of field names to update | User |
|`lock(user_id)` | Returns the locked user after setting its status to `Locked` | User |
|`set_password(user_id,password)` | Returns `true` if the update completes successfully | Boolean |
|`change_password(user_id,current,newpass)` | Returns `true` if the update completes successfully. Needs to be called by the user itself.  | Boolean |
|`set_key(user_id)` | Returns the created API key | String |
|`renew_key(user_id)` | Returns the renewed API key | String |
|`get_key(user_id)` | Returns the API key of the user identified by `user_id` | String |
|`revoke_key(user_id)` | Returns `true` if the API key is revoked successfully | Boolean |

### Examples

The following example shows how to manipulate users:

```python
import json
import uuid

from cortex4py.api import Api
from cortex4py.query import *

api = Api('http://CORTEX_APP_URL:9001', '**API_KEY**')

# List the latest 10 active users
users = api.users.find_all(Eq('status', 'Ok'), range='0-10', sort='-createdAt')

# Display the users' logins and roles
for user in users:
  print('User {} has roles {}'.format(user.name, user.roles))

# Create a new user
rand = str(uuid.uuid4())[:6]
new_user = api.users.create(User({
    'login': 'User-{}'.format(rand),
    'name': 'User {}'.format(rand),
    'roles': ['read', 'analyze'],
    'status': 'Ok',
    'organization': 'demo'
}))

# Display the created user details
print(json.dumps(new_user.json(), indent=2))

# Update the user's name and roles
api.users.update(new_user.id, {
  'name': 'New User',
  'roles': ['read']
})

user_id = new_user.id

# Set user's password
api.users.set_password(user_id, 'password')

# Set user's API Key
key1 = api.users.set_key(user_id)
print(key1)

# Get user's API Key
key = api.users.get_key(user_id)
print(key)

# Renew user's API key
key2 = api.users.renew_key(user_id)
print(key2)

# Compare keys
print(key1 == key2)

# Revoke the user's API keu
api.users.revoke_key(user_id)

# Lock the user
api.users.lock(user_id)

# Get the user details
user = api.users.get_by_id(user_id)

# check some assertions
print(user.hasKey == False)
print(user.hasPassword == True)
print(user.status == 'Locked')
```

## Analyzer Pperations

The `AnalyzersController` class provides a set of methods to handle analyzers.

### Model

An analyzer is an instance of an analyzer definition, and both models share the same fields.

An analyzer definition is represented by the following model class:

| Field | Description | Type |
| --------- | ----------- | ---- |
| `id` | Analyzer ID once enabled within an organization | readonly |
| `analyzerDefinitionId`| Analyzer definition name | readonly |
| `name` | Name of the analyzer | readonly |
| `version` | Version of the analyzer | readonly |
| `description` | Description of the analyzer | readonly |
| `author` | Author of the analyzer | readonly |
| `url` | URL where the analyzer has been published | readonly |
| `license` | License of the analyzer | readonly |
| `dataTypeList` | Allowed datatypes | readonly |
| `configurationItems` | A list that describes the configuration options of the analyzer | readonly |
| `baseConfig` | Base configuration name. This identifies the shared set of configuration with all the analyzer's flavors | readonly |
| `createdBy` | User who enabled the analyzer | computed |
| `updatedAt` | Last update date | computed |
| `updatedBy` | User who last updated the analyzer | computed |

An analyzer is represented by the following model class:

| Field | Description | Type |
| --------- | ----------- | ---- |
| `id` | Analyzer ID once enabled within an organization | readonly |
| `analyzerDefinitionId`| Analyzer definition name | readonly |
| `name` | Name of the analyzer | readonly |
| `version` | Version of the analyzer | readonly |
| `description` | Description of the analyzer | readonly |
| `author` | Author of the analyzer | readonly |
| `url` | URL where the analyzer has been published | readonly |
| `license` | License of the analyzer | readonly |
| `dataTypeList` | Allowed datatypes | readonly |
| `baseConfig` | Base configuration name. This identifies the shared set of configuration with all the analyzer's flavors | readonly |
| `jobCache` | Report cache timeout in minutes, visible for `orgAdmin` users only | writable |
| `rate` | Numeric amount of analyzer calls authorized for the specified `rateUnit`, visible for `orgAdmin` users only | writable |
| `rateUnit` | Period of availability of the rate limite: `Day` or `Month`, visible for `orgAdmin` users only | writable |
| `configuration` |  A JSON object where key/value pairs represent the config names, and their values. It includes the default properties `proxy_http`, `proxy_https`, `auto_extract_artifacts`, `check_tlp`, and `max_tlp`, visible for `orgAdmin` users only | writable |
| `createdBy` | User who enabled the analyzer | computed |
| `updatedAt` | Last update date | computed |
| `updatedBy` | User who last updated the analyzer | computed |

### Methods

| Method | Description | Return type |
| --------- | ----------- | ---- |
|`find_all(query,**kwargs)` | Returns a list of `Analyzer` objects, based on `query`, `range` and `sort` parameters | List[Analyzer] |
|`find_one_by(query,**kwargs)` | Returns the first `Analyzer` object, based on `query` and `sort` parameters | Analyzer |
|`get_by_id(analyzer_id)` | Returns a `Analyzer` by its `id` | Analyzer |
|`get_by_name(name)` | Returns a `Analyzer` by its `name` | Analyzer |
|`get_by_type(data_type)` | Returns a list of available `Analyzer` applicable to the given `data_type` | List[Analyzer] |
|`enable(analyzer_name,config)` | Activate an analyzer and returns its `Analyzer` object | Analyzer |
|`update(analyzer_id)` | Update the configuration of an `Analyzer` and returns the updated version | Analyzer |
|`disable(analyzer_id)` | Removes an analyzer from an organization and returns `true` if it completes successfully | Boolean |
|`run_by_id(analyzer_id,observable,**kwargs)` | Returns a `Job` by its `name` | Job |
|`run_by_name(analyzer_name,observable,**kwargs)` | Runs an analyzer by its name and returns the resulting `Job` | Job |
|`definitions()` | Returns the list of all the analyzer definitions including the enabled and disabled analyzers | List[AnalyzerDefinition] |

### Examples

The following example shows how to manipulate analyzers:

```python
import json

from cortex4py.api import Api
from cortex4py.query import *

api = Api('http://CORTEX_APP_URL:9001', '**API_KEY**')

# Get enabled analyzers
analyzers = api.analyzers.find_all({}, range='all')

# Display enabled analyzers' names
for analyzer in analyzers:
  print('Analyzer {} is enabled'.format(analyzer.name))

# Get enabled analyzers that can run against a domain
domain_analyzers = api.analyzers.get_by_type('domain')

# Enable the analyzer called Test_1_0
analyzer = api.analyzers.enable('Test_1_0', {
  "configuration": {
    "api_key": "XXXXXXXXXXXXXx",
    "proxy_http": "http://localhost:9999",
    "proxy_https": "http://localhost:9999",
    "auto_extract_artifacts": False,
    "check_tlp": True,
    "max_tlp": 2
  },
  "rate": 1000,
  "rateUnit": "Day",
  "jobCache": 5
})

# Print the details of the enaled analyzer
print(json.dumps(analyzer.json(), indent=2))
print(analyzer.analyzerDefinitionId == 'Test_1_0')

# Update the configuration
analyzer_id = analyzer.id
analyzer = api.analyzers.update(analyzer.id, {
  "rate": 100,
  "rateUnit": "Day",
  "jobCache": null,
  "configuration": {
    "api_key": "YYYYYYYYYYY",
    "proxy_http": null,
    "proxy_https": null,
    "auto_extract_artifacts": True,
    "check_tlp": false,
    "max_tlp": null
  }
})

# Run an analyzer against a domain
job1 = api2.analyzers.run_by_name('Test_1_0', {
    'data': 'google.com',
    'dataType': 'domain',
    'tlp': 1,
    'message': 'custom message sent to analyzer',
    'parameters': {
        'key1': 'value1',
        'key2': True,
        'key3': 10
    }
}, force=1)
print(json.dumps(job1.json(), indent=2))

# Run an analyzer against a file
job2 = api2.analyzers.run_by_name('File_Info_2_0', {
    'data': '/tmp/sample.txt',
    'dataType': 'file',
    'tlp': 1
}, force=1)
print(json.dumps(job2.json(), indent=2))

# Disable an analyzer
api.analyzers.disable(analyzer_id)
```

## Job Operations

The `JobsController` class provides a set of methods to handle jobs. A job is the execution of a specific analyzer.

### Model

A job is represented by the following model class:

| Attribute | Description | Type |
| --------- | ----------- | ---- |
| `id` | Job ID | computed |
| `analyzerDefinitionId`| Analyzer definition name | readonly |
| `analyzerId` | Instance ID of the analyzer to which the job is associated  | readonly |
| `organization` | Organization to which the user belongs (set upon account creation) | readonly |
| `analyzerName` | Name of the analyzer to which the job is associated | readonly |
| `dataType` | the datatype of the analyzed observable | readonly |
| `status` | Status of the job (`Waiting`, `InProgress`, `Success`, `Failure`, `Deleted`) | computed |
| `data` | Value of the analyzed observable (does not apply to `file` observables) | readonly |
| `attachment` | JSON object representing `file` observables (does not apply to non-`file` observables). It  defines the`name`, `hashes`, `size`, `contentType` and `id` of the `file` observable | readonly |
| `parameters` | JSON object of key/value pairs set during job creation | readonly |
| `message` | A free text field to set additional text/context for a job | readonly |
| `tlp` | The TLP of the analyzed observable | readonly |
| `report` | The analysy report as a JSON object including `success`, `full`, `summary` and `artifacts` peoperties.<br>In case of failure, the resport contains a `errorMessage` property | readonly |
| `startDate` | Start date | computed |
| `endDate` | End date | computed |
| `createdAt` | Creation date. Please note that a job can be requested but not immediately honored. The actual time at which it is started is the value of `startDate` | computed |
| `createdBy` | User who created the job | computed |
| `updatedAt` | Last update date (only Cortex updates a job when it finishes) | computed |
| `updatedBy` | User who submitted the job and which identity is used by Cortex to update the job once it is finished | computed |

A `JobArtifact` is represented by the following model class:

| Attribute | Description | Type |
| --------- | ----------- | ---- |
| `id` | Artifact ID | computed |
| `dataType` | Artifact data type | readonly |
| `data` | Artifact value | readonly |
| `createdAt` | Creation date. | computed |
| `createdBy` | User who created the job that generated the artifact | computed |

### Methods

| Method | Description | Return type |
| --------- | ----------- | ---- |
|`find_all(query,**kwargs)` | Returns a list of `Job` objects, based on `query`, `range` and `sort` parameters | List[Job] |
|`find_one_by(query,**kwargs)` | Returns the first `Job` object, based on `query` and `sort` parameters | Job |
|`get_by_id(job_id)` | Returns a `Job` by its `id` | Job |
|`get_report(job_id)` | Returns synchronously the `Job` object including its analysis report even if the job is still running | Job |
|`get_report_async(job_id)` | Waits and returns the `Job` object including its analysis report | Job |
|`get_artifacts(job_id)` | Returns a list of the observables that have been extracted from the analysis report  | List[JobArtifact] |
|`delete(job_id)` | Requires `superadmin` role, returns `true` if the delete completes successfully | Boolean |

### Examples

```python
import json

from cortex4py.api import Api
from cortex4py.query import *

api = Api('http://CORTEX_APP_URL:9001', '**API_KEY**')

# Fetch the last 10 successful jobs that have been executed against domain names
query = And(Eq('status', 'Success'), Eq('dataType', 'domain'))
jobs = api.jobs.find_all(query, range='0-10', sort='-createdAt')

# Display summaries of the jobs above
for job in jobs:
  report = api.jobs.get_report(job.id).report
  print('Job summary is {}'.format(json.dumps(report.get('summary', {}))))

  print('Job {} has generated the following artifacts:'.format(job.id))
  artifacts = api.jobs.get_artifacts(job.id)
  for a in artifacts:
    print('- [{}]: {}'.format(a.dataType, a.data))
```
