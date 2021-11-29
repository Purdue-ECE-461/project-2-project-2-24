# flake8: noqa

# import all models into this package
# if you have many models here with many references from one model to another this may
# raise a RecursionError
# to avoid this, import only the models that you directly need like:
# from from openapi_client.model.pet import Pet
# or import this package, but before doing it, use:
# import sys
# sys.setrecursionlimit(n)

from openapi_client.model.authentication_request import AuthenticationRequest
from openapi_client.model.error import Error
from openapi_client.model.package import Package
from openapi_client.model.package_data import PackageData
from openapi_client.model.package_history_entry import PackageHistoryEntry
from openapi_client.model.package_metadata import PackageMetadata
from openapi_client.model.package_query import PackageQuery
from openapi_client.model.package_rating import PackageRating
from openapi_client.model.user import User
from openapi_client.model.user_authentication_info import UserAuthenticationInfo
from openapi_client.model.user_group import UserGroup
