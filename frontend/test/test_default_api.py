"""
    ECE 461 - Fall 2021 - Project 2 - Team 24

    Expanded API for ECE 461/Fall 2021/Project 2/Team 24: A Trustworthy Module Registry  # noqa: E501

    The version of the OpenAPI document: 2.0.0
    Contact: gonza487@purdue.edu
    Generated by: https://openapi-generator.tech
"""


import unittest

import openapi_client
from openapi_client.api.default_api import DefaultApi  # noqa: E501


class TestDefaultApi(unittest.TestCase):
    """DefaultApi unit test stubs"""

    def setUp(self):
        self.api = DefaultApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_auth_token(self):
        """Test case for create_auth_token

        """
        pass

    def test_create_user_group(self):
        """Test case for create_user_group

        Create a UserGroup  # noqa: E501
        """
        pass

    def test_delete_user_group(self):
        """Test case for delete_user_group

        Delete a UserGroup  # noqa: E501
        """
        pass

    def test_get_user_group(self):
        """Test case for get_user_group

        Get a UserGroup  # noqa: E501
        """
        pass

    def test_get_user_groups(self):
        """Test case for get_user_groups

        List All UserGroups  # noqa: E501
        """
        pass

    def test_package_by_name_delete(self):
        """Test case for package_by_name_delete

        Delete all versions of this package.  # noqa: E501
        """
        pass

    def test_package_by_name_get(self):
        """Test case for package_by_name_get

        """
        pass

    def test_package_create(self):
        """Test case for package_create

        """
        pass

    def test_package_delete(self):
        """Test case for package_delete

        Delete this version of the package.  # noqa: E501
        """
        pass

    def test_package_rate(self):
        """Test case for package_rate

        """
        pass

    def test_package_retrieve(self):
        """Test case for package_retrieve

        """
        pass

    def test_package_update(self):
        """Test case for package_update

        Update this version of the package.  # noqa: E501
        """
        pass

    def test_packages_list(self):
        """Test case for packages_list

        Get packages  # noqa: E501
        """
        pass

    def test_registry_reset(self):
        """Test case for registry_reset

        """
        pass

    def test_update_user_group(self):
        """Test case for update_user_group

        Update a UserGroup  # noqa: E501
        """
        pass

    def test_user_create(self):
        """Test case for user_create

        Create a new user  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
