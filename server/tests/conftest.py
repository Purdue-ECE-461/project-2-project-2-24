import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from openapi_server.database import database
from openapi_server.models.package import Package
from openapi_server.models.package_data import PackageData
from openapi_server.models.package_metadata import PackageMetadata
from openapi_server.models.user import User
from openapi_server.models.user_authentication_info import UserAuthenticationInfo

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
def user_auth() -> UserAuthenticationInfo:
    return UserAuthenticationInfo(password="password")



@pytest.fixture
def new_user() -> User:
    return User(name="Matthew", is_admin=False)


@pytest.fixture
def package() -> Package:
    return Package(
        metadata=PackageMetadata(name="PackageName", version="1.2.3", id="5"),
        data=PackageData(content="packagecontent", url="https://www.package.url", js_program="javascript_code;")
    )


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
