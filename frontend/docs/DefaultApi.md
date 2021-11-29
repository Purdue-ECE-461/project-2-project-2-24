# openapi_client.DefaultApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_auth_token**](DefaultApi.md#create_auth_token) | **PUT** /authenticate | 
[**create_user_group**](DefaultApi.md#create_user_group) | **POST** /usergroups | Create a UserGroup
[**delete_user_group**](DefaultApi.md#delete_user_group) | **DELETE** /usergroups/{usergroupId} | Delete a UserGroup
[**get_user_group**](DefaultApi.md#get_user_group) | **GET** /usergroups/{usergroupId} | Get a UserGroup
[**get_user_groups**](DefaultApi.md#get_user_groups) | **GET** /usergroups | List All UserGroups
[**package_by_name_delete**](DefaultApi.md#package_by_name_delete) | **DELETE** /package/byName/{name} | Delete all versions of this package.
[**package_by_name_get**](DefaultApi.md#package_by_name_get) | **GET** /package/byName/{name} | 
[**package_create**](DefaultApi.md#package_create) | **POST** /package | 
[**package_delete**](DefaultApi.md#package_delete) | **DELETE** /package/{id} | Delete this version of the package.
[**package_rate**](DefaultApi.md#package_rate) | **GET** /package/{id}/rate | 
[**package_retrieve**](DefaultApi.md#package_retrieve) | **GET** /package/{id} | 
[**package_update**](DefaultApi.md#package_update) | **PUT** /package/{id} | Update this version of the package.
[**packages_list**](DefaultApi.md#packages_list) | **POST** /packages | Get packages
[**registry_reset**](DefaultApi.md#registry_reset) | **DELETE** /reset | 
[**update_user_group**](DefaultApi.md#update_user_group) | **PUT** /usergroups/{usergroupId} | Update a UserGroup
[**user_create**](DefaultApi.md#user_create) | **POST** /user | Create a new user


# **create_auth_token**
> str create_auth_token(authentication_request)



### Example


```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.authentication_request import AuthenticationRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    authentication_request = AuthenticationRequest(
        user=User(
            name="Alfalfa",
            is_admin=True,
            user_authentication_info=UserAuthenticationInfo(
                password="password_example",
            ),
            user_group=UserGroup(
                name="name_example",
                upload=True,
                search=True,
                download=True,
                register=True,
            ),
        ),
        secret=UserAuthenticationInfo(
            password="password_example",
        ),
    ) # AuthenticationRequest | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.create_auth_token(authentication_request)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->create_auth_token: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authentication_request** | [**AuthenticationRequest**](AuthenticationRequest.md)|  |

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success. |  -  |
**401** | Authentication failed (e.g. no such user or invalid password) |  -  |
**501** | This system does not support authentication. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_user_group**
> create_user_group(x_authorization, user_group)

Create a UserGroup

Creates a new instance of a `UserGroup`.

### Example


```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.user_group import UserGroup
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    x_authorization = "X-Authorization_example" # str | 
    user_group = UserGroup(
        name="name_example",
        upload=True,
        search=True,
        download=True,
        register=True,
    ) # UserGroup | A new `UserGroup` to be created.

    # example passing only required values which don't have defaults set
    try:
        # Create a UserGroup
        api_instance.create_user_group(x_authorization, user_group)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->create_user_group: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_authorization** | **str**|  |
 **user_group** | [**UserGroup**](UserGroup.md)| A new &#x60;UserGroup&#x60; to be created. |

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_user_group**
> delete_user_group(usergroup_id, x_authorization)

Delete a UserGroup

Deletes an existing `UserGroup`.

### Example


```python
import time
import openapi_client
from openapi_client.api import default_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    usergroup_id = "usergroupId_example" # str | A unique identifier for a `UserGroup`.
    x_authorization = "X-Authorization_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Delete a UserGroup
        api_instance.delete_user_group(usergroup_id, x_authorization)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->delete_user_group: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **usergroup_id** | **str**| A unique identifier for a &#x60;UserGroup&#x60;. |
 **x_authorization** | **str**|  |

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user_group**
> UserGroup get_user_group(usergroup_id, x_authorization)

Get a UserGroup

Gets the details of a single instance of a `UserGroup`.

### Example


```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.user_group import UserGroup
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    usergroup_id = "usergroupId_example" # str | A unique identifier for a `UserGroup`.
    x_authorization = "X-Authorization_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Get a UserGroup
        api_response = api_instance.get_user_group(usergroup_id, x_authorization)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->get_user_group: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **usergroup_id** | **str**| A unique identifier for a &#x60;UserGroup&#x60;. |
 **x_authorization** | **str**|  |

### Return type

[**UserGroup**](UserGroup.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful response - returns a single &#x60;UserGroup&#x60;. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user_groups**
> [UserGroup] get_user_groups()

List All UserGroups

Gets a list of all `UserGroup` entities.

### Example


```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.user_group import UserGroup
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # List All UserGroups
        api_response = api_instance.get_user_groups()
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->get_user_groups: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**[UserGroup]**](UserGroup.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful response - returns an array of &#x60;UserGroup&#x60; entities. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **package_by_name_delete**
> package_by_name_delete(name)

Delete all versions of this package.

### Example


```python
import time
import openapi_client
from openapi_client.api import default_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    name = "name_example" # str | 
    x_authorization = "X-Authorization_example" # str |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete all versions of this package.
        api_instance.package_by_name_delete(name)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->package_by_name_delete: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete all versions of this package.
        api_instance.package_by_name_delete(name, x_authorization=x_authorization)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->package_by_name_delete: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**|  |
 **x_authorization** | **str**|  | [optional]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Package is deleted. |  -  |
**400** | No such package. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **package_by_name_get**
> [PackageHistoryEntry] package_by_name_get(name)



Return the history of this package (all versions).

### Example


```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.error import Error
from openapi_client.model.package_history_entry import PackageHistoryEntry
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    name = "name_example" # str | 
    x_authorization = "X-Authorization_example" # str |  (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.package_by_name_get(name)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->package_by_name_get: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.package_by_name_get(name, x_authorization=x_authorization)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->package_by_name_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**|  |
 **x_authorization** | **str**|  | [optional]

### Return type

[**[PackageHistoryEntry]**](PackageHistoryEntry.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Package history |  -  |
**400** | No such package. |  -  |
**0** | unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **package_create**
> PackageMetadata package_create(x_authorization, package)



### Example


```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.package import Package
from openapi_client.model.package_metadata import PackageMetadata
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    x_authorization = "X-Authorization_example" # str | 
    package = Package(
        metadata=PackageMetadata(
            name="name_example",
            version="1.2.3",
            id="id_example",
            sensitive=True,
            secret=True,
        ),
        data=PackageData(
            content="content_example",
            url="url_example",
            js_program="js_program_example",
        ),
    ) # Package | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.package_create(x_authorization, package)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->package_create: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_authorization** | **str**|  |
 **package** | [**Package**](Package.md)|  |

### Return type

[**PackageMetadata**](PackageMetadata.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Success. Check the ID in the returned metadata for the official ID. |  -  |
**400** | Malformed request. |  -  |
**403** | Package exists already. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **package_delete**
> package_delete(id)

Delete this version of the package.

### Example


```python
import time
import openapi_client
from openapi_client.api import default_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    id = "id_example" # str | Package ID
    x_authorization = "X-Authorization_example" # str |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete this version of the package.
        api_instance.package_delete(id)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->package_delete: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete this version of the package.
        api_instance.package_delete(id, x_authorization=x_authorization)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->package_delete: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Package ID |
 **x_authorization** | **str**|  | [optional]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Package is deleted. |  -  |
**400** | No such package. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **package_rate**
> PackageRating package_rate(id)



### Example


```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.package_rating import PackageRating
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    id = "id_example" # str | 
    x_authorization = "X-Authorization_example" # str |  (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.package_rate(id)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->package_rate: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.package_rate(id, x_authorization=x_authorization)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->package_rate: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **x_authorization** | **str**|  | [optional]

### Return type

[**PackageRating**](PackageRating.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Rating. Only use this if each metric was computed successfully. |  -  |
**400** | No such package. |  -  |
**500** | The package rating system choked on at least one of the metrics. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **package_retrieve**
> Package package_retrieve(id)



Return this package.

### Example


```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.package import Package
from openapi_client.model.error import Error
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    id = "id_example" # str | ID of package to fetch
    x_authorization = "X-Authorization_example" # str |  (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.package_retrieve(id)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->package_retrieve: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.package_retrieve(id, x_authorization=x_authorization)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->package_retrieve: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| ID of package to fetch |
 **x_authorization** | **str**|  | [optional]

### Return type

[**Package**](Package.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | pet response |  -  |
**0** | unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **package_update**
> package_update(id, package)

Update this version of the package.

The name, version, and ID must match.  The package contents (from PackageData) will replace the previous contents.

### Example


```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.package import Package
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    id = "id_example" # str | 
    package = Package(
        metadata=PackageMetadata(
            name="name_example",
            version="1.2.3",
            id="id_example",
            sensitive=True,
            secret=True,
        ),
        data=PackageData(
            content="content_example",
            url="url_example",
            js_program="js_program_example",
        ),
    ) # Package | 
    x_authorization = "X-Authorization_example" # str |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Update this version of the package.
        api_instance.package_update(id, package)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->package_update: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Update this version of the package.
        api_instance.package_update(id, package, x_authorization=x_authorization)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->package_update: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **package** | [**Package**](Package.md)|  |
 **x_authorization** | **str**|  | [optional]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success. |  -  |
**400** | Malformed request (e.g. no such package). |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **packages_list**
> [PackageMetadata] packages_list(package_query)

Get packages

Get any packages fitting the query.

### Example


```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.error import Error
from openapi_client.model.package_query import PackageQuery
from openapi_client.model.package_metadata import PackageMetadata
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    package_query = [
        PackageQuery(
            version='''Exact (1.2.3)
Bounded range (1.2.3-2.1.0)
Carat (^1.2.3)
Tilde (~1.2.0)''',
            name="name_example",
        ),
    ] # [PackageQuery] | 
    x_authorization = "X-Authorization_example" # str |  (optional)
    offset = "1" # str | Provide this for pagination. If not provided, returns the first page of results. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get packages
        api_response = api_instance.packages_list(package_query)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->packages_list: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get packages
        api_response = api_instance.packages_list(package_query, x_authorization=x_authorization, offset=offset)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->packages_list: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **package_query** | [**[PackageQuery]**](PackageQuery.md)|  |
 **x_authorization** | **str**|  | [optional]
 **offset** | **str**| Provide this for pagination. If not provided, returns the first page of results. | [optional]

### Return type

[**[PackageMetadata]**](PackageMetadata.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of packages |  * offset -  <br>  |
**0** | unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **registry_reset**
> registry_reset()



### Example


```python
import time
import openapi_client
from openapi_client.api import default_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    x_authorization = "X-Authorization_example" # str |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_instance.registry_reset(x_authorization=x_authorization)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->registry_reset: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_authorization** | **str**|  | [optional]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Registry is reset. |  -  |
**401** | You do not have permission to reset the registry. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_user_group**
> update_user_group(usergroup_id, x_authorization, user_group)

Update a UserGroup

Updates an existing `UserGroup`.

### Example


```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.user_group import UserGroup
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    usergroup_id = "usergroupId_example" # str | A unique identifier for a `UserGroup`.
    x_authorization = "X-Authorization_example" # str | 
    user_group = UserGroup(
        name="name_example",
        upload=True,
        search=True,
        download=True,
        register=True,
    ) # UserGroup | Updated `UserGroup` information.

    # example passing only required values which don't have defaults set
    try:
        # Update a UserGroup
        api_instance.update_user_group(usergroup_id, x_authorization, user_group)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->update_user_group: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **usergroup_id** | **str**| A unique identifier for a &#x60;UserGroup&#x60;. |
 **x_authorization** | **str**|  |
 **user_group** | [**UserGroup**](UserGroup.md)| Updated &#x60;UserGroup&#x60; information. |

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** | Successful response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **user_create**
> User user_create(x_authorization, user)

Create a new user

Create a new registered user. Pass in User in body, and AuthorizationToken in header. AuthorizationToken must belong to user with \"Admin\" privileges.

### Example


```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.user import User
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    x_authorization = "X-Authorization_example" # str | 
    user = User(
        name="Alfalfa",
        is_admin=True,
        user_authentication_info=UserAuthenticationInfo(
            password="password_example",
        ),
        user_group=UserGroup(
            name="name_example",
            upload=True,
            search=True,
            download=True,
            register=True,
        ),
    ) # User | New user to register.

    # example passing only required values which don't have defaults set
    try:
        # Create a new user
        api_response = api_instance.user_create(x_authorization, user)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->user_create: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_authorization** | **str**|  |
 **user** | [**User**](User.md)| New user to register. |

### Return type

[**User**](User.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | User successfully created. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

