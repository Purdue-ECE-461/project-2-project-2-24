import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from openapi_server.database import database
from openapi_server.models.package import Package
from openapi_server.models.package_data import PackageData
from openapi_server.models.package_metadata import PackageMetadata
from openapi_server.models.user import User
from openapi_server.models.user_group import UserGroup
from openapi_server.models.user_authentication_info import UserAuthenticationInfo
from openapi_server.models.authentication_request import AuthenticationRequest

from openapi_server.database import utils

from openapi_server.main import app as application


@pytest.fixture
def app() -> FastAPI:
    application.dependency_overrides = {}

    return application


@pytest.fixture
def client(app) -> TestClient:
    return TestClient(app)


@pytest.fixture
def default_user_authentication_info() -> UserAuthenticationInfo:
    return UserAuthenticationInfo(password="correcthorsebatterystaple123(!__+@**(A")


@pytest.fixture
def new_user_authentication_info() -> UserAuthenticationInfo:
    return UserAuthenticationInfo(password="new_user_password")


@pytest.fixture
def new_user_password(new_user_authentication_info) -> str:
    return new_user_authentication_info.password


@pytest.fixture
def admin_user_group() -> UserGroup:
    return UserGroup(
        id=1,
        name="Admins",
        upload=True,
        search=True,
        download=True,
        create_user=True
    )


@pytest.fixture
def default_user(default_user_authentication_info, admin_user_group) -> User:
    return User(
        id=1,
        name="ece461defaultadminuser",
        is_admin=True,
        user_authentication_info=default_user_authentication_info,
        user_group=admin_user_group
    )


@pytest.fixture
def new_user(new_user_authentication_info, admin_user_group) -> User:
    return User(
        name="Aiden",
        is_admin=True,
        user_authentication_info=new_user_authentication_info,
        user_group=admin_user_group
    )


@pytest.fixture
def default_username(default_user) -> str:
    return default_user.name


@pytest.fixture
def password() -> str:
    return "password"


@pytest.fixture
def user_auth(password) -> UserAuthenticationInfo:
    return UserAuthenticationInfo(password=password)


@pytest.fixture
def default_auth_request(default_user, default_user_authentication_info) -> AuthenticationRequest:
    return AuthenticationRequest(user=default_user, secret=default_user_authentication_info)


@pytest.fixture
def table() -> str:
    return "packages"


@pytest.fixture
def int_id_table() -> str:
    return "tokens"


@pytest.fixture
def package() -> Package:
    return Package(
        metadata=PackageMetadata(name="debug-js", version="4.3.3", id="debug"),
        data=PackageData(content="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")
    )


@pytest.fixture
def package_to_ingest() -> Package:
    return Package(
        metadata=PackageMetadata(name="debug-js", version="4.3.4", id="debug"),
        data=PackageData(url="https://github.com/debug-js/debug")
    )


@pytest.fixture
def default_token() -> str:
    return "default_token"


@pytest.fixture
def package_id(package) -> str:
    return package.metadata.id


@pytest.fixture
def package_name(package) -> str:
    return package.metadata.name


@pytest.fixture
def package_ingest_id(package_to_ingest) -> str:
    return package_to_ingest.metadata.id


@pytest.fixture
def package_ingest_name(package_to_ingest) -> str:
    return package_to_ingest.metadata.name


@pytest.fixture
def admin_user_group_name(admin_user_group) -> str:
    return admin_user_group.name


@pytest.fixture
def js_program() -> str:
    return "javascript_program;"


@pytest.fixture
def valid_query() -> str:
    return f"""
        SELECT COUNT(*) FROM `ece-461-proj-2-24.module_registry.packages`
    """


@pytest.fixture
def invalid_query() -> str:
    return f"""
        SELECT COUNT(invalid_column) FROM `ece-461-proj-2-24.module_registry.packages`
    """
