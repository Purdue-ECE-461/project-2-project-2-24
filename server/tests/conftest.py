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
    return UserGroup(name="Admin", upload=True, search=True, download=True, create_user=True)


@pytest.fixture
def default_user(default_user_authentication_info, admin_user_group) -> User:
    return User(
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
def package() -> Package:
    return Package(
        metadata=PackageMetadata(name="PackageName", version="1.2.3", id="5"),
        data=PackageData(content="packagecontent", url="https://www.package.url", js_program="javascript_code;")
    )


@pytest.fixture
def default_token() -> str:
    return utils.db_hash("default_token")


@pytest.fixture
def package_id(package) -> str:
    return package.metadata.name + "_" + package.metadata.version


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
