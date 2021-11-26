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

from openapi_server.main import app as application


@pytest.fixture
def app() -> FastAPI:
    application.dependency_overrides = {}

    return application


@pytest.fixture
def client(app) -> TestClient:
    return TestClient(app)


@pytest.fixture
def user() -> User:
    return User(name="Aiden", is_admin=True)


@pytest.fixture
def user_group() -> UserGroup:
    return UserGroup(name="Admin", upload=True, search=True, download=True, register=True)


@pytest.fixture
def username(user) -> str:
    return user.name


@pytest.fixture
def user_auth() -> UserAuthenticationInfo:
    return UserAuthenticationInfo(password="password")


@pytest.fixture
def auth_request(user, user_auth) -> AuthenticationRequest:
    return AuthenticationRequest(user=user, secret=user_auth)


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
def token() -> str:
    return "87d3c9d0817af26f70281302e34fa8b79753b4ef48f2d63303cb79f45928c2cf"


@pytest.fixture
def package_id(package) -> str:
    return package.metadata.name + "_" + package.metadata.version


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
