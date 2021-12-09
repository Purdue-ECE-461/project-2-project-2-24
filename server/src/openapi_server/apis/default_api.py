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


def token_from_auth(auth):
    token = ""
    try:
        token = auth.split()[-1]
    except:
        token = Error(code=400, message="Missing x-authorization header data!")
    return token


def prettify_metadata(metadata):
    return {
        "Name": metadata.name,
        "Version": metadata.version,
        "ID": metadata.id,
        "Sensitive": metadata.sensitive,
        "Secret": metadata.secret
    }


def prettify_data(data):
    return {
        "Content": data.content,
        "URL": data.url,
        "JSProgram": data.js_program
    }


def prettify_rating(rating):
    return {
        "RampUp": rating.ramp_up,
        "Correctness": rating.correctness,
        "BusFactor": rating.bus_factor,
        "ResponsiveMaintainer": rating.responsive_maintainer,
        "LicenseScore": rating.license_score,
        "GoodPinnningPractice": rating.good_pinning_practice
    }


def prettify_package(package):
    package.metadata = prettify_metadata(package.metadata)
    package.data = prettify_data(package.data)
    return package


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
    request: Request,
    response: Response,
    authentication_request: AuthenticationRequest = Body(None, description=""),
) -> str:
    logger.info("CREATE_AUTH_TOKEN REQUEST:\n")
    logger.info(await stringify_request(request))
    new_token = db.create_new_token(authentication_request)
    if isinstance(new_token, Error):
        response.status_code = new_token.code
    logger.info(new_token)
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
    request: Request,
    response: Response,
    x_authorization: str = Header(None, description=""),
    user_group: UserGroup = Body(None, description="A new UserGroup to be created."),
) -> None:
    """Creates a new instance of a UserGroup."""
    logger.info("CREATE_USER_GROUP REQUEST:\n")
    logger.info(await stringify_request(request))
    token = token_from_auth(x_authorization)
    if isinstance(token, Error):
        response.status_code = token.code
        return token
    # First check if token is expired
    expired = db.check_token_expiration(token)
    if isinstance(expired, Error):
        response.status_code = expired.code
        logger.warning(expired)
        return expired
    user = db.get_user_from_token(token)
    if isinstance(user, Error):
        response.status_code = user.code
        logger.warning(user)
        return user
    if not user.user_group.create_user:
        err = Error(code=401, message="Not authorized to create a new user group!")
        response.status_code = err.code
        logger.warning(err)
        return err
    result = db.create_new_user_group(user_group)
    if isinstance(result, Error):
        response.status_code = result.code
    # Now decrement remaining token uses
    decrement = db.decrement_token_interactions(token)
    if isinstance(decrement, Error):
        response.status_code = decrement.code
        logger.warning(decrement)
        return decrement
    logger.info(result)
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
    request: Request,
    response: Response,
    usergroupId: str = Path(None, description="A unique identifier for a &#x60;UserGroup&#x60;."),
    x_authorization: str = Header(None, description=""),
) -> None:
    """Deletes an existing UserGroup."""
    logger.info("DELETE_USER_GROUP REQUEST:\n")
    logger.info(await stringify_request(request))
    token = token_from_auth(x_authorization)
    if isinstance(token, Error):
        response.status_code = token.code
        return token
    # First check if token is expired
    expired = db.check_token_expiration(token)
    if isinstance(expired, Error):
        response.status_code = expired.code
        logger.warning(expired)
        return expired
    # TODO: DO STUFF HERE
    # Now decrement remaining token uses
    decrement = db.decrement_token_interactions(token)
    if isinstance(decrement, Error):
        response.status_code = decrement.code
        logger.warning(decrement)
        return decrement
    err = Error(code="501", message="Not implemented!")
    response.status_code = err.code
    logger.warning(err)
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
    request: Request,
    response: Response,
    usergroupId: str = Path(None, description="A unique identifier for a &#x60;UserGroup&#x60;."),
    x_authorization: str = Header(None, description=""),
) -> UserGroup:
    """Gets the details of a single instance of a UserGroup."""
    logger.info("GET_USER_GROUP REQUEST:\n")
    logger.info(await stringify_request(request))
    token = token_from_auth(x_authorization)
    if isinstance(token, Error):
        response.status_code = token.code
        return token
    # First check if token is expired
    expired = db.check_token_expiration(token)
    if isinstance(expired, Error):
        response.status_code = expired.code
        logger.warning(expired)
        return expired
    # TODO: DO STUFF HERE
    # Now decrement remaining token uses
    decrement = db.decrement_token_interactions(token)
    if isinstance(decrement, Error):
        response.status_code = decrement.code
        logger.warning(decrement)
        return decrement
    err = Error(code="501", message="Not implemented!")
    response.status_code = err.code
    logger.warning(err)
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
    logger.info("GET_USER_GROUPS REQUEST:\n")
    err = Error(code="501", message="Not implemented!")
    response.status_code = err.code
    logger.warning(err)
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
    request: Request,
    response: Response,
    name: str = Path(None, description=""),
    x_authorization: str = Header(None, description=""),
) -> None:
    logger.info("PACKAGE_BY_NAME_DELETE REQUEST:\n")
    logger.info(await stringify_request(request))
    token = token_from_auth(x_authorization)
    if isinstance(token, Error):
        response.status_code = token.code
        return token
    # First check if token is expired
    expired = db.check_token_expiration(token)
    if isinstance(expired, Error):
        response.status_code = expired.code
        logger.warning(expired)
        return expired
    user = db.get_user_from_token(token)
    if isinstance(user, Error):
        response.status_code = user.code
        logger.warning(user)
        return user
    if not user.user_group.upload:
        err = Error(code=401, message="Not authorized to delete a package!")
        response.status_code = err.code
        logger.warning(err)
        return err
    result = db.delete_package_by_name(name)
    if isinstance(result, Error):
        response.status_code = result.code
    # Now decrement remaining token uses
    decrement = db.decrement_token_interactions(token)
    if isinstance(decrement, Error):
        response.status_code = decrement.code
        logger.warning(decrement)
        return decrement
    logger.info(result)
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
    request: Request,
    response: Response,
    name: str = Path(None, description=""),
    x_authorization: str = Header(None, description=""),
) -> List[PackageHistoryEntry]:
    """Return the history of this package (all versions)."""
    logger.info("PACKAGE_BY_NAME_GET REQUEST:\n")
    logger.info(await stringify_request(request))
    token = token_from_auth(x_authorization)
    if isinstance(token, Error):
        response.status_code = token.code
        return token
    # First check if token is expired
    expired = db.check_token_expiration(token)
    if isinstance(expired, Error):
        response.status_code = expired.code
        logger.warning(expired)
        return expired
    user = db.get_user_from_token(token)
    if isinstance(user, Error):
        response.status_code = user.code
        logger.warning(user)
        return user
    if not user.user_group.search:
        err = Error(code=401, message="Not authorized to get a package!")
        response.status_code = err.code
        logger.warning(err)
        return err
    packages = db.get_package_by_name(name)
    if isinstance(packages, Error):
        response.status_code = packages.code
    # Now decrement remaining token uses
    decrement = db.decrement_token_interactions(token)
    if isinstance(decrement, Error):
        response.status_code = decrement.code
        logger.warning(decrement)
        return decrement
    for i in range(len(packages)):
        if isinstance(packages[i], Package):
            packages[i] = prettify_package(packages[i])
    logger.info(packages)
    return packages


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
    request: Request,
    response: Response,
    x_authorization: str = Header(None, description=""),
    package: Package = Body(None, description=""),
) -> PackageMetadata:
    logger.info("PACKAGE_CREATE REQUEST:\n")
    logger.info(await stringify_request(request))
    token = token_from_auth(x_authorization)
    if isinstance(token, Error):
        response.status_code = token.code
        return token
    # First check if token is expired
    expired = db.check_token_expiration(token)
    if isinstance(expired, Error):
        response.status_code = expired.code
        logger.warning(expired)
        return expired
    user = db.get_user_from_token(token)
    if isinstance(user, Error):
        response.status_code = user.code
        logger.warning(user)
        return user
    if not user.user_group.upload:
        err = Error(code=401, message="Not authorized to upload a package!")
        response.status_code = err.code
        logger.warning(err)
        return err
    metadata = db.upload_package(user, package)
    if isinstance(metadata, Error):
        response.status_code = metadata.code
    # Now decrement remaining token uses
    decrement = db.decrement_token_interactions(token)
    if isinstance(decrement, Error):
        response.status_code = decrement.code
        logger.warning(decrement)
        return decrement
    if isinstance(metadata, PackageMetadata):
        metadata = prettify_metadata(metadata)
    logger.info(metadata)
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
    request: Request,
    response: Response,
    id: str = Path(None, description="Package ID"),
    x_authorization: str = Header(None, description=""),
) -> None:
    logger.info("PACKAGE_DELETE REQUEST:\n")
    logger.info(await stringify_request(request))
    token = token_from_auth(x_authorization)
    if isinstance(token, Error):
        response.status_code = token.code
        return token
    # First check if token is expired
    expired = db.check_token_expiration(token)
    if isinstance(expired, Error):
        response.status_code = expired.code
        logger.warning(expired)
        return expired
    user = db.get_user_from_token(token)
    if isinstance(user, Error):
        response.status_code = user.code
        logger.warning(user)
        return user
    if not user.user_group.upload:
        err = Error(code=401, message="Not authorized to delete a package!")
        response.status_code = err.code
        logger.warning(err)
        return err
    result = db.delete_package(id)
    if isinstance(result, Error):
        response.status_code = result.code
    # Now decrement remaining token uses
    decrement = db.decrement_token_interactions(token)
    if isinstance(decrement, Error):
        response.status_code = decrement.code
        logger.warning(decrement)
        return decrement
    logger.info(result)
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
    request: Request,
    response: Response,
    id: str = Path(None, description=""),
    x_authorization: str = Header(None, description=""),
) -> PackageRating:
    logger.info("PACKAGE_RATE REQUEST:\n")
    logger.info(await stringify_request(request))
    token = token_from_auth(x_authorization)
    if isinstance(token, Error):
        response.status_code = token.code
        return token
    # First check if token is expired
    expired = db.check_token_expiration(token)
    if isinstance(expired, Error):
        response.status_code = expired.code
        logger.warning(expired)
        return expired
    user = db.get_user_from_token(token)
    if isinstance(user, Error):
        response.status_code = user.code
        logger.warning(user)
        return user
    if not user.user_group.search:
        err = Error(code=401, message="Not authorized to rate a package!")
        response.status_code = err.code
        logger.warning(err)
        return err
    rating = db.rate_package(id)
    if isinstance(rating, Error):
        response.status_code = rating.code
    # Now decrement remaining token uses
    decrement = db.decrement_token_interactions(token)
    if isinstance(decrement, Error):
        response.status_code = decrement.code
        logger.warning(decrement)
        return decrement
    if isinstance(rating, PackageRating):
        rating = prettify_rating(rating)
    logger.info(rating)
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
    request: Request,
    response: Response,
    id: str = Path(None, description="ID of package to fetch"),
    x_authorization: str = Header(None, description=""),
) -> Package:
    """Return this package."""
    logger.info("PACKAGE_RETRIEVE REQUEST:\n")
    logger.info(await stringify_request(request))
    token = token_from_auth(x_authorization)
    if isinstance(token, Error):
        response.status_code = token.code
        return token
    # First check if token is expired
    expired = db.check_token_expiration(token)
    if isinstance(expired, Error):
        response.status_code = expired.code
        logger.warning(expired)
        return expired
    user = db.get_user_from_token(token)
    if isinstance(user, Error):
        response.status_code = user.code
        logger.warning(user)
        return user
    if not user.user_group.download:
        err = Error(code=401, message="Not authorized to retrieve a package!")
        response.status_code = err.code
        logger.warning(err)
        return err
    package = db.download_package(id)
    if isinstance(package, Error):
        response.status_code = package.code
    # Now decrement remaining token uses
    decrement = db.decrement_token_interactions(token)
    if isinstance(decrement, Error):
        response.status_code = decrement.code
        logger.warning(decrement)
        return decrement
    if isinstance(package, Package):
        package = prettify_package(package)
    logger.info(package)
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
    request: Request,
    response: Response,
    id: str = Path(None, description=""),
    package: Package = Body(None, description=""),
    x_authorization: str = Header(None, description=""),
) -> None:
    """The name, version, and ID must match.  The package contents (from PackageData) will replace the previous contents."""
    logger.info("PACKAGE_UPDATE REQUEST:\n")
    logger.info(await stringify_request(request))
    token = token_from_auth(x_authorization)
    if isinstance(token, Error):
        response.status_code = token.code
        return token
    # First check if token is expired
    expired = db.check_token_expiration(token)
    if isinstance(expired, Error):
        response.status_code = expired.code
        logger.warning(expired)
        return expired
    user = db.get_user_from_token(token)
    if isinstance(user, Error):
        response.status_code = user.code
        logger.warning(user)
        return user
    if not user.user_group.upload:
        err = Error(code=401, message="Not authorized to update a package!")
        response.status_code = err.code
        logger.warning(err)
        return err
    results = db.update_package(user, id, package)
    if isinstance(results, Error):
        response.status_code = results.code
    # Now decrement remaining token uses
    decrement = db.decrement_token_interactions(token)
    if isinstance(decrement, Error):
        response.status_code = decrement.code
        logger.warning(decrement)
        return decrement
    logger.info(results)
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
    x_authorization: str = Header(None, description=""),
    offset: str = Query(None, description="Provide this for pagination. If not provided, returns the first page of results."),
) -> List[PackageMetadata]:
    """Get any packages fitting the query."""
    logger.info("PACKAGES_LIST REQUEST:\n")
    logger.info(await stringify_request(request))
    token = token_from_auth(x_authorization)
    if isinstance(token, Error):
        response.status_code = token.code
        return token
    # First check if token is expired
    expired = db.check_token_expiration(token)
    if isinstance(expired, Error):
        response.status_code = expired.code
        logger.warning(expired)
        return expired
    # Now check if user is authorized to search database
    user = db.get_user_from_token(token)
    if isinstance(user, Error):
        response.status_code = user.code
        logger.warning(user)
        return user
    if not user.user_group.search:
        err = Error(code=401, message="Not authorized to search the registry!")
        response.status_code = err.code
        logger.warning(err)
        return err
    packages = db.get_page_of_packages(package_query, offset)
    if isinstance(packages, Error):
        response.status_code = packages.code
    # Now decrement remaining token uses
    decrement = db.decrement_token_interactions(token)
    if isinstance(decrement, Error):
        response.status_code = decrement.code
        logger.warning(decrement)
        return decrement
    logger.info(packages)
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
    request: Request,
    response: Response,
    x_authorization: str = Header(None, description=""),
) -> None:
    logger.info("REGISTRY_RESET REQUEST:\n")
    logger.info(await stringify_request(request))
    token = token_from_auth(x_authorization)
    if isinstance(token, Error):
        response.status_code = token.code
        return token
    # First check if token is expired
    expired = db.check_token_expiration(token)
    if isinstance(expired, Error):
        response.status_code = expired.code
        logger.warning(expired)
        return expired
    user = db.get_user_from_token(token)
    if isinstance(user, Error):
        response.status_code = user.code
        logger.warning(user)
        return user
    if not user.user_group.create_user:
        err = Error(code=401, message="Not authorized to reset the registry!")
        response.status_code = err.code
        logger.warning(err)
        return err
    reset = db.reset_registry()
    if isinstance(reset, Error):
        response.status_code = reset.code
    # Don't decrement token for registry reset
    logger.info(reset)
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
    request: Request,
    response: Response,
    usergroupId: str = Path(None, description="A unique identifier for a &#x60;UserGroup&#x60;."),
    x_authorization: str = Header(None, description=""),
    user_group: UserGroup = Body(None, description="Updated UserGroup information."),
) -> None:
    """Updates an existing UserGroup."""
    logger.info("UPDATE_USER_GROUP REQUEST:\n")
    logger.info(await stringify_request(request))
    token = token_from_auth(x_authorization)
    if isinstance(token, Error):
        response.status_code = token.code
        return token
    # First check if token is expired
    expired = db.check_token_expiration(token)
    if isinstance(expired, Error):
        response.status_code = expired.code
        logger.warning(expired)
        return expired
    # TODO: DO STUFF HERE
    # Now decrement remaining token uses
    decrement = db.decrement_token_interactions(token)
    if isinstance(decrement, Error):
        response.status_code = decrement.code
        logger.warning(decrement)
        return decrement
    err = Error(code="501", message="Not implemented!")
    response.status_code = err.code
    logger.warning(err)
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
    request: Request,
    response: Response,
    x_authorization: str = Header(None, description=""),
    user: User = Body(None, description="New user to register."),
) -> User:
    """Create a new registered user. Pass in User in body, and AuthorizationToken in header. AuthorizationToken must belong to user with \&quot;Admin\&quot; privileges."""
    logger.info("CREATE_USER REQUEST:\n")
    logger.info(await stringify_request(request))
    token = token_from_auth(x_authorization)
    if isinstance(token, Error):
        response.status_code = token.code
        return token
    # First check if token is expired
    expired = db.check_token_expiration(token)
    if isinstance(expired, Error):
        response.status_code = expired.code
        logger.warning(expired)
        return expired
    # TODO: DO STUFF HERE
    # Now decrement remaining token uses
    decrement = db.decrement_token_interactions(token)
    if isinstance(decrement, Error):
        response.status_code = decrement.code
        logger.warning(decrement)
        return decrement
    err = Error(code="501", message="Not implemented!")
    response.status_code = err.code
    logger.warning(err)
    return err
