from __future__ import absolute_import
from openapi_server.database import database
from openapi_server.models.package import Package
from openapi_server.models.package_data import PackageData
from openapi_server.models.package_metadata import PackageMetadata
from openapi_server.models.user import User
from dotenv import load_dotenv

load_dotenv()

db = database.Database()

user = User(name="Aiden", is_admin=True)
new_user = User(name="Matthew", is_admin=False)
package =  Package(
    metadata= PackageMetadata(name="PackageName", version="1.2.3", id="5"), 
    data= PackageData(content="packagecontent", url="https://www.package.url", js_program="javascript_code;")
)


def test_get_user_id_from_token():
    return "TODO"


def test_upload_package():
    db.upload_package(token="example_token", package=package)


def test_upload_js_program():
    return "TODO"


def test_create_new_user():
    return "TODO"


def test_gen_new_integer_id():
    return "TODO"


def test_get_user_group_id():
    return "TODO"


def test_get_user_id():
    return "TODO"


def test_package_id_exists():
    return "TODO"


def test_gen_new_package_id():
    return "TODO"


def test_package_exists():
    return "TODO"


def test_execute_query():
    return "TODO"


if __name__ == "__main__":
    test_get_user_id_from_token()
    test_upload_js_program()
    test_create_new_user()
    test_gen_new_integer_id()
    test_get_user_group_id()
    test_get_user_id()
    test_package_id_exists()
    test_gen_new_package_id()
    test_package_exists()
    test_execute_query()

    test_upload_package()
