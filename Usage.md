# How to use Cortex4py
This document aims to provide the details of how to use Cortex4py library to write custom scripts handling Cortex 2 apis.

Cortex4py 2.0.0+ required Python 3.

## Table of Contents
  * [Introduction](#introduction)
    * [Migration](#migration)
    * [Proxy and certificate verification](#proxy-and-certificate-verification)    
  * [Organization operations](#organization-operations)    
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

`verif_cert` could be True/False or a string path to the certificate file

