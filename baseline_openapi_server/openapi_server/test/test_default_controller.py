# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.authentication_request import AuthenticationRequest  # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.package import Package  # noqa: E501
from openapi_server.models.package_history_entry import PackageHistoryEntry  # noqa: E501
from openapi_server.models.package_metadata import PackageMetadata  # noqa: E501
from openapi_server.models.package_query import PackageQuery  # noqa: E501
from openapi_server.models.package_rating import PackageRating  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_create_auth_token(self):
        """Test case for create_auth_token

        
        """
        authentication_request = {
  "Secret" : {
    "password" : "password"
  },
  "User" : {
    "name" : "Alfalfa",
    "isAdmin" : true
  }
}
        headers = { 
        }
        response = self.client.open(
            '/authenticate',
            method='PUT',
            headers=headers,
            data=json.dumps(authentication_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_package_by_name_delete(self):
        """Test case for package_by_name_delete

        Delete all versions of this package.
        """
        headers = { 
            'x_authorization': 'x_authorization_example',
        }
        response = self.client.open(
            '/package/byName/{name}'.format(name='name_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_package_by_name_get(self):
        """Test case for package_by_name_get

        
        """
        headers = { 
            'x_authorization': 'x_authorization_example',
        }
        response = self.client.open(
            '/package/byName/{name}'.format(name='name_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_package_create(self):
        """Test case for package_create

        
        """
        package = {
  "metadata" : {
    "Version" : "1.2.3",
    "ID" : "ID",
    "Name" : "Name"
  },
  "data" : {
    "Content" : "Content",
    "JSProgram" : "JSProgram",
    "URL" : "URL"
  }
}
        headers = { 
            'x_authorization': 'x_authorization_example',
        }
        response = self.client.open(
            '/package',
            method='POST',
            headers=headers,
            data=json.dumps(package),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_package_delete(self):
        """Test case for package_delete

        Delete this version of the package.
        """
        headers = { 
            'x_authorization': 'x_authorization_example',
        }
        response = self.client.open(
            '/package/{id}'.format(id='id_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_package_rate(self):
        """Test case for package_rate

        
        """
        headers = { 
            'x_authorization': 'x_authorization_example',
        }
        response = self.client.open(
            '/package/{id}/rate'.format(id='id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_package_retrieve(self):
        """Test case for package_retrieve

        
        """
        headers = { 
            'x_authorization': 'x_authorization_example',
        }
        response = self.client.open(
            '/package/{id}'.format(id='id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_package_update(self):
        """Test case for package_update

        Update this version of the package.
        """
        package = {
  "metadata" : {
    "Version" : "1.2.3",
    "ID" : "ID",
    "Name" : "Name"
  },
  "data" : {
    "Content" : "Content",
    "JSProgram" : "JSProgram",
    "URL" : "URL"
  }
}
        headers = { 
            'x_authorization': 'x_authorization_example',
        }
        response = self.client.open(
            '/package/{id}'.format(id='id_example'),
            method='PUT',
            headers=headers,
            data=json.dumps(package),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_packages_list(self):
        """Test case for packages_list

        Get packages
        """
        package_query = {
  "Version" : "Exact (1.2.3)\nBounded range (1.2.3-2.1.0)\nCarat (^1.2.3)\nTilde (~1.2.0)",
  "Name" : "Name"
}
        query_string = [('offset', 'offset_example')]
        headers = { 
            'x_authorization': 'x_authorization_example',
        }
        response = self.client.open(
            '/packages',
            method='GET',
            headers=headers,
            data=json.dumps(package_query),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_registry_reset(self):
        """Test case for registry_reset

        
        """
        headers = { 
            'x_authorization': 'x_authorization_example',
        }
        response = self.client.open(
            '/reset',
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
