import connexion
import six

from openapi_server.models.authentication_request import AuthenticationRequest  # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.package import Package  # noqa: E501
from openapi_server.models.package_history_entry import PackageHistoryEntry  # noqa: E501
from openapi_server.models.package_metadata import PackageMetadata  # noqa: E501
from openapi_server.models.package_query import PackageQuery  # noqa: E501
from openapi_server.models.package_rating import PackageRating  # noqa: E501
from openapi_server import util


def create_auth_token(authentication_request):  # noqa: E501
    """create_auth_token

     # noqa: E501

    :param authentication_request: 
    :type authentication_request: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        authentication_request = AuthenticationRequest.from_dict(connexion.request.get_json())  # noqa: E501
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
    return 'do some magic!'


def package_create(x_authorization, package):  # noqa: E501
    """package_create

     # noqa: E501

    :param x_authorization: 
    :type x_authorization: str
    :param package: 
    :type package: dict | bytes

    :rtype: PackageMetadata
    """
    if connexion.request.is_json:
        package = Package.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def package_delete(id, x_authorization=None):  # noqa: E501
    """Delete this version of the package.

     # noqa: E501

    :param id: Package ID
    :type id: str
    :param x_authorization: 
    :type x_authorization: str

    :rtype: None
    """
    return 'do some magic!'


def package_rate(id, x_authorization=None):  # noqa: E501
    """package_rate

     # noqa: E501

    :param id: 
    :type id: str
    :param x_authorization: 
    :type x_authorization: str

    :rtype: PackageRating
    """
    return 'do some magic!'


def package_retrieve(id, x_authorization=None):  # noqa: E501
    """package_retrieve

    Return this package. # noqa: E501

    :param id: ID of package to fetch
    :type id: str
    :param x_authorization: 
    :type x_authorization: str

    :rtype: Package
    """
    return 'do some magic!'


def package_update(id, package, x_authorization=None):  # noqa: E501
    """Update this version of the package.

    The name, version, and ID must match.  The package contents (from PackageData) will replace the previous contents. # noqa: E501

    :param id: 
    :type id: str
    :param package: 
    :type package: dict | bytes
    :param x_authorization: 
    :type x_authorization: str

    :rtype: None
    """
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
    if connexion.request.is_json:
        package_query = [PackageQuery.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501
    return 'do some magic!'


def registry_reset(x_authorization=None):  # noqa: E501
    """registry_reset

     # noqa: E501

    :param x_authorization: 
    :type x_authorization: str

    :rtype: None
    """
    return 'do some magic!'
