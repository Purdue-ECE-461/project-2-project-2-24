# PackageData

This is a \"union\" type. - On package upload, either Content or URL should be set. - On package update, exactly one field should be set. - On download, the Content field should be set.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | **str** | Package contents. This is the zip file uploaded by the user. (Encoded as text using a Base64 encoding).  This will be a zipped version of an npm package&#39;s GitHub repository, minus the \&quot;.git/\&quot; directory.\&quot; It will, for example, include the \&quot;package.json\&quot; file that can be used to retrieve the project homepage.  See https://docs.npmjs.com/cli/v7/configuring-npm/package-json#homepage. | [optional] 
**url** | **str** | Package URL (for use in public ingest). | [optional] 
**js_program** | **str** | A JavaScript program (for use with sensitive modules). | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


