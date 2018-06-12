# How to use Cortex4py
This document aims to provide the details of how to use Cortex4py library to write custom scripts handling Cortex 2 apis.

Cortex4py 2.0.0+ required Python 3.

## Table of Contents
  * [Introduction](#introduction)
    * [Migration](#migration)
    * [Proxy and certificate verification](#proxy-and-certificate-verification)
    * [Backward compatibility](#backward-compatibility)
    * [Exception handling](#exception-handling)       
  * [Organization operations](#organization-operations)
    * [Model](#model-1)
    * [Methods](#methods-1)
    * [Examples](#examples-1)
    
  * [User operations](#user-operations)
  * [Analyzer operations](#analyzer-operations)
  * [Job operations](#job-operations)
    
    
## Introduction

Cortex4py 2.0.0+ is a new version of the library, that is only compatible with Cortex V2.

It introduces support authentication and covers almost all the available APIs, including administration APIs.

### Migration

For developers who have already written scripts evolving `cortex4py` for Cortex v1, we tried to keep the already available methods, but we recommend using the new classes and methods.

The existing scripts must be updated to  to add authentication.

For Cortex v1, to instantiate an API object, developer used to write the following code:

````python
from cortex4py.api import CortexApi

api = CortexApi('http://CORTEX_APP_URL.1:9000')
````

This code must be replaced by something like below:

```python
from cortex4py.api import Api

api = Api('http://CORTEX_APP_URL:9001', '**API_KEY**')
```

### Proxy and certificate verification

Cortex4py 2.0.0+ allows specifying a proxy configuration the custom script requires a proxy, and an option to enable/disable certificate verification.

```python
from cortex4py.api import Api

api = Api('http://CORTEX_APP_URL:9001', '**API_KEY**', proxies={
    'http': 'http://PROXY_URL:PROXY_PORT',
    'https': 'http://PROXY_URL:PROXY_PORT'
}, verify_cert=False)
```

`verify_cert` could be True/False or a string path to the certificate file

**Note**: `verify_cert` replaces the `cert` argument that has been deprecated.

### Backward compatibility

Cortex4py 2.0.0+ implements the methods that were available within the old version of the library:

```python
from cortex4py.api import Api

api = Api('http://CORTEX_APP_URL:9001', '**API_KEY**')

analyzers = api.get_analyzers('ip')
job = api.run_analyzer('Abuse_Finder_2_0', 'domain', 2, 'google.com')
job_with_report = api.get_job_report('XXXXXX', timeout='Inf')        
job_deleted = api.delete_job('XXXXXX')
```

These methods are now deprecated.

### Exception handling

All the libraries operations generates a `cortex4py.exceptions.CortexException` exception, that has a specific error messages and wraps the original exception:

| Error message | Description |
| --------- | ----------- |
| `Resource not found` | A 404 error occurred |
| `Authentication error` | A 401 error occurred |
| `Authorization error` | A 403 error occurred |
| `Invalid input exception` | A 400 error occurred |
| `Cortex service is unavailable` | Connection issue, Cortex is not available |
| `Cortex request exception` | A 500 error occurred |
| `Unexpected exception` | An unhandled error occurred | 


## Organization operations

The `OrganizationController` class provides a set of methods to handle organizations:

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

