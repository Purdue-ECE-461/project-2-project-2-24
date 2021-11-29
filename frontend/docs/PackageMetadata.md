# PackageMetadata

The \"Name\" and \"Version\" are used as a unique identifier pair when uploading a package.  The \"ID\" is used as an internal identifier for interacting with existing packages.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Name of a package.  - Names should only use typical \&quot;keyboard\&quot; characters. - The name \&quot;*\&quot; is reserved. See the &#x60;/packages&#x60; API for its meaning. | 
**version** | **str** | Package version | 
**id** | **str** |  | 
**sensitive** | **bool** | Sensitivity of package.  If True, js_program must be run before allowing download of the package. | [optional] 
**secret** | **bool** | Secrecy of package.  If True, package can only be queried by member of User Group that uploaded it. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


