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


router = APIRouter()
db = Database()


def token_from_auth(auth):
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
    x_authorization: str = Header(None, description="", convert_underscores=False),
    user_group: UserGroup = Body(None, description="A new UserGroup to be created."),
) -> None:
    """Creates a new instance of a UserGroup."""
    ...


@router.delete(
    "/usergroups/{usergroupId}",
    responses={
        204: {"description": "Successful response."},
    },
    tags=["default"],
    summary="Delete a UserGroup",
)
async def delete_user_group(
    usergroupId: str = Path(None, description="A unique identifier for a &#x60;UserGroup&#x60;."),
    x_authorization: str = Header(None, description="", convert_underscores=False),
) -> None:
    """Deletes an existing UserGroup."""
    ...


@router.get(
    "/usergroups/{usergroupId}",
    responses={
        200: {"model": UserGroup, "description": "Successful response - returns a single UserGroup."},
    },
    tags=["default"],
    summary="Get a UserGroup",
)
async def get_user_group(
    usergroupId: str = Path(None, description="A unique identifier for a &#x60;UserGroup&#x60;."),
    x_authorization: str = Header(None, description="", convert_underscores=False),
) -> UserGroup:
    """Gets the details of a single instance of a UserGroup."""
    ...


@router.get(
    "/usergroups",
    responses={
        200: {"model": List[UserGroup], "description": "Successful response - returns an array of UserGroup entities."},
    },
    tags=["default"],
    summary="List All UserGroups",
)
async def get_user_groups(
) -> List[UserGroup]:
    """Gets a list of all UserGroup entities."""
    ...


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
    name: str = Path(None, description=""),
    x_authorization: str = Header(None, description="", convert_underscores=False),
) -> None:
    ...


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
    name: str = Path(None, description=""),
    x_authorization: str = Header(None, description="", convert_underscores=False),
) -> List[PackageHistoryEntry]:
    """Return the history of this package (all versions)."""
    ...


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
    user = db.get_user_from_token(token_from_auth(x_authorization))
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
    id: str = Path(None, description="Package ID"),
    x_authorization: str = Header(None, description="", convert_underscores=False),
) -> None:
    ...


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
    id: str = Path(None, description=""),
    x_authorization: str = Header(None, description="", convert_underscores=False),
) -> PackageRating:
    ...


@router.get(
    "/package/{id}",
    responses={
        200: {"model": Package, "description": "pet response"},
        200: {"model": Error, "description": "unexpected error"},
    },
    tags=["default"],
)
async def package_retrieve(
    id: str = Path(None, description="ID of package to fetch"),
    x_authorization: str = Header(None, description="", convert_underscores=False),
) -> Package:
    """Return this package."""
    ...


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
    user = db.get_user_from_token(token_from_auth(x_authorization))
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
    package_query: List[PackageQuery] = Body(None, description=""),
    x_authorization: str = Header(None, description="", convert_underscores=False),
    offset: str = Query(None, description="Provide this for pagination. If not provided, returns the first page of results."),
) -> List[PackageMetadata]:
    """Get any packages fitting the query."""
    ...


@router.delete(
    "/reset",
    responses={
        200: {"description": "Registry is reset."},
        401: {"description": "You do not have permission to reset the registry."},
    },
    tags=["default"],
)
async def registry_reset(
    x_authorization: str = Header(None, description="", convert_underscores=False),
) -> None:
    ...


@router.put(
    "/usergroups/{usergroupId}",
    responses={
        202: {"description": "Successful response."},
    },
    tags=["default"],
    summary="Update a UserGroup",
)
async def update_user_group(
    usergroupId: str = Path(None, description="A unique identifier for a &#x60;UserGroup&#x60;."),
    x_authorization: str = Header(None, description="", convert_underscores=False),
    user_group: UserGroup = Body(None, description="Updated UserGroup information."),
) -> None:
    """Updates an existing UserGroup."""
    ...


@router.post(
    "/user",
    responses={
        200: {"model": User, "description": "User successfully created."},
    },
    tags=["default"],
    summary="Create a new user",
)
async def user_create(
    x_authorization: str = Header(None, description="", convert_underscores=False),
    user: User = Body(None, description="New user to register."),
) -> User:
    """Create a new registered user. Pass in User in body, and AuthorizationToken in header. AuthorizationToken must belong to user with \&quot;Admin\&quot; privileges."""
    ...
