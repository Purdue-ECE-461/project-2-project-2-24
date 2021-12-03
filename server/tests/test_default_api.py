# coding: utf-8

from fastapi.testclient import TestClient

from openapi_server.models.authentication_request import AuthenticationRequest  # noqa: F401
from openapi_server.models.error import Error  # noqa: F401
from openapi_server.models.package import Package  # noqa: F401
from openapi_server.models.package_history_entry import PackageHistoryEntry  # noqa: F401
from openapi_server.models.package_metadata import PackageMetadata  # noqa: F401
from openapi_server.models.package_query import PackageQuery  # noqa: F401
from openapi_server.models.package_rating import PackageRating  # noqa: F401
from openapi_server.models.user import User  # noqa: F401
from openapi_server.models.user_group import UserGroup  # noqa: F401

from openapi_server.database import utils


def test_registry_reset(client: TestClient):
    """Test case for registry_reset


    """

    headers = {
        "x_authorization": "default_token",
    }
    response = client.request(
        "DELETE",
        "/reset",
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    assert response.status_code == 200


def test_create_auth_token(client: TestClient):
    """Test case for create_auth_token

    
    """
    authentication_request = {
        "secret": {
            "password": "correcthorsebatterystaple123(!__+@**(A"
        },
        "user": {
            "name": "ece461defaultadminuser",
            "is_admin": 1,
            "id": 1,
            "user_authentication_info": {
                "password": "correcthorsebatterystaple123(!__+@**(A"
            },
            "user_group": {
                "name": "Admins",
                "upload": 1,
                "search": 1,
                "download": 1,
                "create_user": 1}
        }
    }

    headers = {
    }
    response = client.request(
        "PUT",
        "/authenticate",
        headers=headers,
        json=authentication_request,
    )

    # uncomment below to assert the status code of the HTTP response
    assert response.status_code == 200


def test_create_user_group(client: TestClient):
    """Test case for create_user_group

    Create a UserGroup
    """
    user_group = {
        "name": "Admins",
        "upload": 1,
        "search": 1,
        "download": 1,
        "create_user": 1
    }

    headers = {
        "x_authorization": 'default_token',
    }
    response = client.request(
        "POST",
        "/usergroups",
        headers=headers,
        json=user_group,
    )

    # uncomment below to assert the status code of the HTTP response
    assert response.status_code == 200


def test_delete_user_group(client: TestClient):
    """Test case for delete_user_group

    Delete a UserGroup
    """

    headers = {
        "x_authorization": 'default_token',
    }
    response = client.request(
        "DELETE",
        "/usergroups/{usergroupId}".format(usergroupId='usergroup_id_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    assert response.status_code == 200


def test_get_user_group(client: TestClient):
    """Test case for get_user_group

    Get a UserGroup
    """

    headers = {
        "x_authorization": 'default_token',
    }
    response = client.request(
        "GET",
        "/usergroups/{usergroupId}".format(usergroupId='usergroup_id_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    assert response.status_code == 200


def test_get_user_groups(client: TestClient):
    """Test case for get_user_groups

    List All UserGroups
    """

    headers = {
    }
    response = client.request(
        "GET",
        "/usergroups",
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    assert response.status_code == 200


def test_package_by_name_delete(client: TestClient):
    """Test case for package_by_name_delete

    Delete all versions of this package.
    """

    headers = {
        "x_authorization": 'default_token',
    }
    response = client.request(
        "DELETE",
        "/package/byName/{name}".format(name='name_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    assert response.status_code == 200


def test_package_by_name_get(client: TestClient):
    """Test case for package_by_name_get

    
    """

    headers = {
        "x_authorization": 'default_token',
    }
    response = client.request(
        "GET",
        "/package/byName/{name}".format(name='name_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    assert response.status_code == 200


def test_package_create(client: TestClient):
    """Test case for package_create

    
    """
    package = {"metadata": {"secret": 1, "version": "1.2.3", "sensitive": 1, "id": "ID", "name": "Name"},
               "data": {"content": "Content", "js_program": "JSProgram"}}

    headers = {
        "x_authorization": "default_token",
    }
    response = client.request(
        "POST",
        "/package",
        headers=headers,
        json=package,
    )

    # uncomment below to assert the status code of the HTTP response
    assert response.status_code == 201


def test_package_delete(client: TestClient):
    """Test case for package_delete

    Delete this version of the package.
    """

    headers = {
        "x_authorization": 'default_token',
    }
    response = client.request(
        "DELETE",
        "/package/{id}".format(id='id_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    assert response.status_code == 200


def test_package_rate(client: TestClient):
    """Test case for package_rate

    
    """

    headers = {
        "x_authorization": 'default_token',
    }
    response = client.request(
        "GET",
        "/package/{id}/rate".format(id='id_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    assert response.status_code == 200


def test_package_retrieve(client: TestClient):
    """Test case for package_retrieve

    
    """

    headers = {
        "x_authorization": 'default_token',
    }
    response = client.request(
        "GET",
        "/package/{id}".format(id='id_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    assert response.status_code == 200


def test_package_update(client: TestClient):
    """Test case for package_update

    Update this version of the package.
    """
    package = {"metadata": {"secret": 1, "version": "1.2.3", "sensitive": 1, "id": "ID", "name": "Name"},
               "data": {"content": "Content", "js_program": "JSProgram", "url": "URL"}}

    headers = {
        "x_authorization": "default_token",
    }
    response = client.request(
        "PUT",
        "/package/{id}".format(id='ID'),
        headers=headers,
        json=package,
    )

    # uncomment below to assert the status code of the HTTP response
    assert response.status_code == 200


def test_packages_list(client: TestClient):
    """Test case for packages_list

    Get packages
    """
    package_query = [
        {"version": "Exact (1.2.3)\nBounded range (1.2.3-2.1.0)\nCarat (^1.2.3)\nTilde (~1.2.0)", "name": "Name"}]
    params = [("offset", '0')]
    headers = {
        "x_authorization": 'default_token',
    }
    response = client.request(
        "POST",
        "/packages",
        headers=headers,
        json=package_query,
        params=params,
    )

    # uncomment below to assert the status code of the HTTP response
    assert response.status_code == 200


def test_update_user_group(client: TestClient):
    """Test case for update_user_group

    Update a UserGroup
    """
    user_group = {"name": "Admins", "upload": 1, "search": 1, "download": 1, "create_user": 1}

    headers = {
        "x_authorization": 'default_token',
    }
    response = client.request(
        "PUT",
        "/usergroups/{usergroupId}".format(usergroupId='usergroup_id_example'),
        headers=headers,
        json=user_group,
    )

    # uncomment below to assert the status code of the HTTP response
    assert response.status_code == 200


def test_user_create(client: TestClient):
    """Test case for user_create

    Create a new user
    """
    user = {"name": "Alfalfa", "is_admin": 1, "id": 1, "user_authentication_info": {"password": "password"},
            "user_group": {"name": "Admins", "upload": 1, "search": 1, "download": 1, "create_user": 1}}

    headers = {
        "x_authorization": "default_token",
    }
    response = client.request(
        "POST",
        "/user",
        headers=headers,
        json=user,
    )

    # uncomment below to assert the status code of the HTTP response
    assert response.status_code == 200
