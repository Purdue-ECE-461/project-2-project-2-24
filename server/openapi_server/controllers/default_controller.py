import connexion
import six

from openapi_server.models.authentication_request import AuthenticationRequest  # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.package import Package  # noqa: E501
from openapi_server.models.package_history_entry import PackageHistoryEntry  # noqa: E501
from openapi_server.models.package_metadata import PackageMetadata  # noqa: E501
from openapi_server.models.package_query import PackageQuery  # noqa: E501
from openapi_server.models.package_rating import PackageRating  # noqa: E501
from openapi_server.models.user import User # noqa: E501
from openapi_server import util
from openapi_server.database import database

from flask import request

db = database.Database()


def get_x_authorization_token():
    return dict(request.headers)["X-Authorization"].split()[-1]


def create_auth_token(authentication_request):  # noqa: E501
    """create_auth_token

     # noqa: E501

    :param authentication_request: 
    :type authentication_request: dict | bytes

    :rtype: str
    """

    print("\create_auth_token:\n")
    print(locals())
    print()

    return 'do some magic!'


def package_by_name_delete(name, x_authorization=None):  # noqa: E501
    """Delete all versions of this package.

     # noqa: E501

    :param name: 
    :type name: str
    :param x_authorization: 
    :type x_authorization: str

    :rtype: None
    """

    x_authorization_token = get_x_authorization_token()

    print("\package_by_name_delete:\n")
    print(locals())
    print()

    return 'do some magic!'


def package_by_name_get(name, x_authorization=None):  # noqa: E501
    """package_by_name_get

    Return the history of this package (all versions). # noqa: E501

    :param name: 
    :type name: str
    :param x_authorization: 
    :type x_authorization: str

    :rtype: List[PackageHistoryEntry]
    """

    x_authorization_token = get_x_authorization_token()

    print("\package_by_name_get:\n")
    print(locals())
    print()

    return 'do some magic!'


def package_create(package, x_authorization=None):  # noqa: E501
    """package_create

     # noqa: E501

    :param x_authorization: 
    :type x_authorization: str
    :param package: 
    :type package: dict | bytes

    :rtype: PackageMetadata
    """

    x_authorization_token = get_x_authorization_token()

    print("\package_create:\n")
    print(locals())
    print()

    return db.upload_package(token=x_authorization_token, package=package)
    

def package_delete(package_id, x_authorization=None):  # noqa: E501
    """Delete this version of the package.

     # noqa: E501

    :param package_id: Package ID
    :type package_id: str
    :param x_authorization: 
    :type x_authorization: str

    :rtype: None
    """

    x_authorization_token = get_x_authorization_token()

    print("\package_delete:\n")
    print(locals())
    print()

    return 'do some magic!'


def package_rate(package_id, x_authorization=None):  # noqa: E501
    """package_rate

     # noqa: E501

    :param package_id: 
    :type package_id: str
    :param x_authorization: 
    :type x_authorization: str

    :rtype: PackageRating
    """

    x_authorization_token = get_x_authorization_token()

    print("\package_rate:\n")
    print(locals())
    print()

    return 'do some magic!'


def package_retrieve(package_id=None, x_authorization=None):  # noqa: E501
    """package_retrieve

    Return this package. # noqa: E501

    :param package_id: ID of package to fetch
    :type package_id: str
    :param x_authorization: 
    :type x_authorization: str

    :rtype: Package
    """

    x_authorization_token = get_x_authorization_token()

    print("\package_retrieve:\n")
    print(locals())
    print()

    return 'do some magic!'


def package_update(package_id, package, x_authorization=None):  # noqa: E501
    """Update this version of the package.

    The name, version, and ID must match.  The package contents (from PackageData) will replace the previous contents. # noqa: E501

    :param package_id: 
    :type package_id: str
    :param package: 
    :type package: dict | bytes
    :param x_authorization: 
    :type x_authorization: str

    :rtype: None
    """

    x_authorization_token = get_x_authorization_token()

    print("\package_update:\n")
    print(locals())
    print()

    if connexion.request.is_json:
        package = Package.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def packages_list(package_query, x_authorization=None, offset=None):  # noqa: E501
    """Get packages

    Get any packages fitting the query. # noqa: E501

    :param package_query: 
    :type package_query: list | bytes
    :param x_authorization: 
    :type x_authorization: str
    :param offset: Provide this for pagination. If not provided, returns the first page of results.
    :type offset: str

    :rtype: List[PackageMetadata]
    """

    x_authorization_token = get_x_authorization_token()

    print("\npackages_list:\n")
    print(locals())
    print()

    return 'do some magic!'


def registry_reset(x_authorization=None):  # noqa: E501
    """registry_reset

     # noqa: E501

    :param x_authorization: 
    :type x_authorization: str

    :rtype: None
    """

    x_authorization_token = get_x_authorization_token()

    print("\nregistry_reset:\n")
    print(locals())
    print()

    return 'do some magic!'
