"""
    ECE 461 - Fall 2021 - Project 2 - Team 24

    Expanded API for ECE 461/Fall 2021/Project 2/Team 24: A Trustworthy Module Registry  # noqa: E501

    The version of the OpenAPI document: 2.0.0
    Contact: gonza487@purdue.edu
    Generated by: https://openapi-generator.tech
"""


import sys
import unittest

import openapi_client
from openapi_client.model.user_authentication_info import UserAuthenticationInfo
from openapi_client.model.user_group import UserGroup
globals()['UserAuthenticationInfo'] = UserAuthenticationInfo
globals()['UserGroup'] = UserGroup
from openapi_client.model.user import User


class TestUser(unittest.TestCase):
    """User unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testUser(self):
        """Test User"""
        # FIXME: construct object with mandatory attributes with example values
        # model = User()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
