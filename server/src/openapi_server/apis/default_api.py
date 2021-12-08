# coding: utf-8

from typing import Dict, List  # noqa: F401

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    Path,
    Query,
    Response,
    Request,
    Security,
    status,
)

from openapi_server.models.extra_models import TokenModel  # noqa: F401
from openapi_server.models.authentication_request import AuthenticationRequest
from openapi_server.models.error import Error
from openapi_server.models.package import Package
from openapi_server.models.package_history_entry import PackageHistoryEntry
from openapi_server.models.package_metadata import PackageMetadata
from openapi_server.models.package_query import PackageQuery
from openapi_server.models.package_rating import PackageRating
from openapi_server.models.user import User
from openapi_server.models.user_group import UserGroup
from openapi_server.database.database import Database

from logging.config import dictConfig
import logging
from openapi_server.models.log_conf import LogConfig
dictConfig(LogConfig().dict())
logger = logging.getLogger("openapi_server")

router = APIRouter()
db = Database()


async def stringify_request(request):
    output = ""
    output += f"request header       : {dict(request.headers.items())}\n"
    output += f"request query params : {dict(request.query_params.items())}\n"
    try:
        output += f"request json         : {await request.json()}\n"
    except Exception as err:
        # could not parse json
        output += f"request body         : {await request.body()}\n"
    return output


async def token_from_auth(auth):
    return auth.split()[-1]


@router.put(
    "/authenticate",
    responses={
        200: {"model": str, "description": "Success."},
        401: {"description": "Authentication failed (e.g. no such user or invalid password)"},
        501: {"description": "This system does not support authentication."},
    },
    tags=["default"],
)
async def create_auth_token(
    response: Response,
    authentication_request: AuthenticationRequest = Body(None, description=""),
) -> str:
    new_token = db.create_new_token(authentication_request)
    if isinstance(new_token, Error):
        response.status_code = new_token.code
    return new_token


@router.post(
    "/usergroups",
    responses={
        201: {"description": "Successful response."},
    },
    tags=["default"],
    summary="Create a UserGroup",
)
async def create_user_group(
    response: Response,
    x_authorization: str = Header(None, description="", convert_underscores=False),
    user_group: UserGroup = Body(None, description="A new UserGroup to be created."),
) -> None:
    """Creates a new instance of a UserGroup."""
    token = token_from_auth(x_authorization)
    # First check if token is expired
    expired = db.check_token_expiration(token)
    if isinstance(expired, Error):
        response.status_code = expired.code
        return expired
    user = db.get_user_from_token(token)
    if isinstance(user, Error):
        response.status_code = user.code
        return user
    if not user.user_group.create_user:
        err = Error(code=401, message="Not authorized to create a new user group!")
        response.status_code = err.code
        return err
    result = db.create_new_user_group(user_group)
    if isinstance(result, Error):
        response.status_code = result.code
    # Now decrement remaining token uses
    decrement = db.decrement_token_interactions(token)
    if isinstance(decrement, Error):
        response.status_code = decrement.code
        return decrement
    return result


@router.delete(
    "/usergroups/{usergroupId}",
    responses={
        204: {"description": "Successful response."},
    },
    tags=["default"],
    summary="Delete a UserGroup",
)
async def delete_user_group(
    response: Response,
    usergroupId: str = Path(None, description="A unique identifier for a &#x60;UserGroup&#x60;."),
    x_authorization: str = Header(None, description="", convert_underscores=False),
) -> None:
    """Deletes an existing UserGroup."""
    token = token_from_auth(x_authorization)
    # First check if token is expired
    expired = db.check_token_expiration(token)
    if isinstance(expired, Error):
        response.status_code = expired.code
        return expired
    # TODO: DO STUFF HERE
    # Now decrement remaining token uses
    decrement = db.decrement_token_interactions(token)
    if isinstance(decrement, Error):
        response.status_code = decrement.code
        return decrement
    err = Error(code="501", message="Not implemented!")
    response.status_code = err.code
    return err


@router.get(
    "/usergroups/{usergroupId}",
    responses={
        200: {"model": UserGroup, "description": "Successful response - returns a single UserGroup."},
    },
    tags=["default"],
    summary="Get a UserGroup",
)
async def get_user_group(
    response: Response,
    usergroupId: str = Path(None, description="A unique identifier for a &#x60;UserGroup&#x60;."),
    x_authorization: str = Header(None, description="", convert_underscores=False),
) -> UserGroup:
    """Gets the details of a single instance of a UserGroup."""
    token = token_from_auth(x_authorization)
    # First check if token is expired
    expired = db.check_token_expiration(token)
    if isinstance(expired, Error):
        response.status_code = expired.code
        return expired
    # TODO: DO STUFF HERE
    # Now decrement remaining token uses
    decrement = db.decrement_token_interactions(token)
    if isinstance(decrement, Error):
        response.status_code = decrement.code
        return decrement
    err = Error(code="501", message="Not implemented!")
    response.status_code = err.code
    return err


@router.get(
    "/usergroups",
    responses={
        200: {"model": List[UserGroup], "description": "Successful response - returns an array of UserGroup entities."},
    },
    tags=["default"],
    summary="List All UserGroups",
)
async def get_user_groups(
    response: Response
) -> List[UserGroup]:
    """Gets a list of all UserGroup entities."""
    err = Error(code="501", message="Not implemented!")
    response.status_code = err.code
    return err


@router.delete(
    "/package/byName/{name}",
    responses={
        200: {"description": "Package is deleted."},
        400: {"description": "No such package."},
    },
    tags=["default"],
    summary="Delete all versions of this package.",
)
async def package_by_name_delete(
    response: Response,
    name: str = Path(None, description=""),
    x_authorization: str = Header(None, description="", convert_underscores=False),
) -> None:
    token = token_from_auth(x_authorization)
    # First check if token is expired
    expired = db.check_token_expiration(token)
    if isinstance(expired, Error):
        response.status_code = expired.code
        return expired
    user = db.get_user_from_token(token)
    if isinstance(user, Error):
        response.status_code = user.code
        return user
    if not user.user_group.upload:
        err = Error(code=401, message="Not authorized to delete a package!")
        response.status_code = err.code
        return err
    result = db.delete_package_by_name(name)
    if isinstance(result, Error):
        response.status_code = result.code
    # Now decrement remaining token uses
    decrement = db.decrement_token_interactions(token)
    if isinstance(decrement, Error):
        response.status_code = decrement.code
        return decrement
    return result


@router.get(
    "/package/byName/{name}",
    responses={
        200: {"model": List[PackageHistoryEntry], "description": "Package history"},
        400: {"description": "No such package."},
        200: {"model": Error, "description": "unexpected error"},
    },
    tags=["default"],
)
async def package_by_name_get(
    response: Response,
    name: str = Path(None, description=""),
    x_authorization: str = Header(None, description="", convert_underscores=False),
) -> List[PackageHistoryEntry]:
    """Return the history of this package (all versions)."""
    token = token_from_auth(x_authorization)
    # First check if token is expired
    expired = db.check_token_expiration(token)
    if isinstance(expired, Error):
        response.status_code = expired.code
        return expired
    user = db.get_user_from_token(token)
    if isinstance(user, Error):
        response.status_code = user.code
        return user
    if not user.user_group.search:
        err = Error(code=401, message="Not authorized to get a package!")
        response.status_code = err.code
        return err
    package = db.get_package_by_name(name)
    if isinstance(package, Error):
        response.status_code = package.code
    # Now decrement remaining token uses
    decrement = db.decrement_token_interactions(token)
    if isinstance(decrement, Error):
        response.status_code = decrement.code
        return decrement
    return package


@router.post(
    "/package",
    responses={
        201: {"model": PackageMetadata, "description": "Success. Check the ID in the returned metadata for the official ID."},
        400: {"description": "Malformed request."},
        403: {"description": "Package exists already."},
    },
    tags=["default"],
    # Default status code:
    status_code=201
)
async def package_create(
    response: Response,
    x_authorization: str = Header(None, description="", convert_underscores=False),
    package: Package = Body(None, description=""),
) -> PackageMetadata:
    token = token_from_auth(x_authorization)
    # First check if token is expired
    expired = db.check_token_expiration(token)
    if isinstance(expired, Error):
        response.status_code = expired.code
        return expired
    user = db.get_user_from_token(token)
    if isinstance(user, Error):
        response.status_code = user.code
        return user
    if not user.user_group.upload:
        err = Error(code=401, message="Not authorized to upload a package!")
        response.status_code = err.code
        return err
    metadata = db.upload_package(user, package)
    if isinstance(metadata, Error):
        response.status_code = metadata.code
    # Now decrement remaining token uses
    decrement = db.decrement_token_interactions(token)
    if isinstance(decrement, Error):
        response.status_code = decrement.code
        return decrement
    return metadata


@router.delete(
    "/package/{id}",
    responses={
        200: {"description": "Package is deleted."},
        400: {"description": "No such package."},
    },
    tags=["default"],
    summary="Delete this version of the package.",
)
async def package_delete(
    response: Response,
    id: str = Path(None, description="Package ID"),
    x_authorization: str = Header(None, description="", convert_underscores=False),
) -> None:
    token = token_from_auth(x_authorization)
    # First check if token is expired
    expired = db.check_token_expiration(token)
    if isinstance(expired, Error):
        response.status_code = expired.code
        return expired
    user = db.get_user_from_token(token)
    if isinstance(user, Error):
        response.status_code = user.code
        return user
    if not user.user_group.upload:
        err = Error(code=401, message="Not authorized to delete a package!")
        response.status_code = err.code
        return err
    result = db.delete_package(id)
    if isinstance(result, Error):
        response.status_code = result.code
    # Now decrement remaining token uses
    decrement = db.decrement_token_interactions(token)
    if isinstance(decrement, Error):
        response.status_code = decrement.code
        return decrement
    return result


@router.get(
    "/package/{id}/rate",
    responses={
        200: {"model": PackageRating, "description": "Rating. Only use this if each metric was computed successfully."},
        400: {"description": "No such package."},
        500: {"description": "The package rating system choked on at least one of the metrics."},
    },
    tags=["default"],
)
async def package_rate(
    response: Response,
    id: str = Path(None, description=""),
    x_authorization: str = Header(None, description="", convert_underscores=False),
) -> PackageRating:
    token = token_from_auth(x_authorization)
    # First check if token is expired
    expired = db.check_token_expiration(token)
    if isinstance(expired, Error):
        response.status_code = expired.code
        return expired
    user = db.get_user_from_token(token)
    if isinstance(user, Error):
        response.status_code = user.code
        return user
    if not user.user_group.search:
        err = Error(code=401, message="Not authorized to rate a package!")
        response.status_code = err.code
        return err
    rating = db.rate_package(id)
    if isinstance(rating, Error):
        response.status_code = rating.code
    # Now decrement remaining token uses
    decrement = db.decrement_token_interactions(token)
    if isinstance(decrement, Error):
        response.status_code = decrement.code
        return decrement
    return rating


@router.get(
    "/package/{id}",
    responses={
        200: {"model": Package, "description": "pet response"},
        200: {"model": Error, "description": "unexpected error"},
    },
    tags=["default"],
)
async def package_retrieve(
    response: Response,
    id: str = Path(None, description="ID of package to fetch"),
    x_authorization: str = Header(None, description="", convert_underscores=False),
) -> Package:
    """Return this package."""
    token = token_from_auth(x_authorization)
    # First check if token is expired
    expired = db.check_token_expiration(token)
    if isinstance(expired, Error):
        response.status_code = expired.code
        return expired
    user = db.get_user_from_token(token)
    if isinstance(user, Error):
        response.status_code = user.code
        return user
    if not user.user_group.download:
        err = Error(code=401, message="Not authorized to retrieve a package!")
        response.status_code = err.code
        return err
    package = db.download_package(id)
    if isinstance(package, Error):
        response.status_code = package.code
    # Now decrement remaining token uses
    decrement = db.decrement_token_interactions(token)
    if isinstance(decrement, Error):
        response.status_code = decrement.code
        return decrement
    return package
  
      
@router.put(
    "/package/{id}",
    responses={
        200: {"description": "Success."},
        400: {"description": "Malformed request (e.g. no such package)."},
    },
    tags=["default"],
    summary="Update this version of the package.",
)
async def package_update(
    response: Response,
    id: str = Path(None, description=""),
    package: Package = Body(None, description=""),
    x_authorization: str = Header(None, description="", convert_underscores=False),
) -> None:
    """The name, version, and ID must match.  The package contents (from PackageData) will replace the previous contents."""
    token = token_from_auth(x_authorization)
    # First check if token is expired
    expired = db.check_token_expiration(token)
    if isinstance(expired, Error):
        response.status_code = expired.code
        return expired
    user = db.get_user_from_token(token)
    if isinstance(user, Error):
        response.status_code = user.code
        return user
    if not user.user_group.upload:
        err = Error(code=401, message="Not authorized to update a package!")
        response.status_code = err.code
        return err
    results = db.update_package(user, id, package)
    if isinstance(results, Error):
        response.status_code = results.code
    # Now decrement remaining token uses
    decrement = db.decrement_token_interactions(token)
    if isinstance(decrement, Error):
        response.status_code = decrement.code
        return decrement
    return results


@router.post(
    "/packages",
    responses={
        200: {"model": List[PackageMetadata], "description": "List of packages"},
        200: {"model": Error, "description": "unexpected error"},
    },
    tags=["default"],
    summary="Get packages",
)
async def packages_list(
    request: Request,
    response: Response,
    package_query: List[PackageQuery] = Body(None, description=""),
    x_authorization: str = Header(None, description="", convert_underscores=False),
    offset: str = Query(None, description="Provide this for pagination. If not provided, returns the first page of results."),
) -> List[PackageMetadata]:
    """Get any packages fitting the query."""
    logger.info(locals())
    logger.info(stringify_request(request))
    token = token_from_auth(x_authorization)
    # First check if token is expired
    expired = db.check_token_expiration(token)
    if isinstance(expired, Error):
        response.status_code = expired.code
        return expired
    # Now check if user is authorized to search database
    user = db.get_user_from_token(token)
    if isinstance(user, Error):
        response.status_code = user.code
        return user
    if not user.user_group.search:
        err = Error(code=401, message="Not authorized to search the registry!")
        response.status_code = err.code
        return err
    packages = db.get_page_of_packages(package_query, offset)
    if isinstance(packages, Error):
        response.status_code = packages.code
    # Now decrement remaining token uses
    decrement = db.decrement_token_interactions(token)
    if isinstance(decrement, Error):
        response.status_code = decrement.code
        return decrement
    return packages


@router.delete(
    "/reset",
    responses={
        200: {"description": "Registry is reset."},
        401: {"description": "You do not have permission to reset the registry."},
    },
    tags=["default"],
)
async def registry_reset(
    response: Response,
    x_authorization: str = Header(None, description="", convert_underscores=False),
) -> None:
    token = token_from_auth(x_authorization)
    # First check if token is expired
    expired = db.check_token_expiration(token)
    if isinstance(expired, Error):
        response.status_code = expired.code
        return expired
    user = db.get_user_from_token(token)
    if isinstance(user, Error):
        response.status_code = user.code
        return user
    if not user.user_group.create_user:
        err = Error(code=401, message="Not authorized to reset the registry!")
        response.status_code = err.code
        return err
    reset = db.reset_registry()
    if isinstance(reset, Error):
        response.status_code = reset.code
    # Don't decrement token for registry reset
    return reset


@router.put(
    "/usergroups/{usergroupId}",
    responses={
        202: {"description": "Successful response."},
    },
    tags=["default"],
    summary="Update a UserGroup",
)
async def update_user_group(
    response: Response,
    usergroupId: str = Path(None, description="A unique identifier for a &#x60;UserGroup&#x60;."),
    x_authorization: str = Header(None, description="", convert_underscores=False),
    user_group: UserGroup = Body(None, description="Updated UserGroup information."),
) -> None:
    """Updates an existing UserGroup."""
    token = token_from_auth(x_authorization)
    # First check if token is expired
    expired = db.check_token_expiration(token)
    if isinstance(expired, Error):
        response.status_code = expired.code
        return expired
    # TODO: DO STUFF HERE
    # Now decrement remaining token uses
    decrement = db.decrement_token_interactions(token)
    if isinstance(decrement, Error):
        response.status_code = decrement.code
        return decrement
    err = Error(code="501", message="Not implemented!")
    response.status_code = err.code
    return err


@router.post(
    "/user",
    responses={
        200: {"model": User, "description": "User successfully created."},
    },
    tags=["default"],
    summary="Create a new user",
)
async def user_create(
    response: Response,
    x_authorization: str = Header(None, description="", convert_underscores=False),
    user: User = Body(None, description="New user to register."),
) -> User:
    """Create a new registered user. Pass in User in body, and AuthorizationToken in header. AuthorizationToken must belong to user with \&quot;Admin\&quot; privileges."""
    token = token_from_auth(x_authorization)
    # First check if token is expired
    expired = db.check_token_expiration(token)
    if isinstance(expired, Error):
        response.status_code = expired.code
        return expired
    # TODO: DO STUFF HERE
    # Now decrement remaining token uses
    decrement = db.decrement_token_interactions(token)
    if isinstance(decrement, Error):
        response.status_code = decrement.code
        return decrement
    err = Error(code="501", message="Not implemented!")
    response.status_code = err.code
    return err
