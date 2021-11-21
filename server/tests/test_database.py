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
    print("\nTESTING: Get user ID from token")
    print()
    print("TODO")


def test_upload_package():
    print("\nTESTING: Upload package")
    print()
    print(db.upload_package(token="example_token", package=package))


def test_upload_js_program():
    print("\nTESTING: Upload js program")
    print()
    print("TODO")


def test_create_new_user():
    print("\nTESTING: Create new user")
    print()
    print("TODO")


def test_gen_new_integer_id():
    print("\nTESTING: Generate new integer ID")
    print()
    print("TODO")


def test_get_user_group_id():
    print("\nTESTING: Get user group ID")
    print()
    print("TODO")


def test_get_user_id():
    print("\nTESTING: Get user ID")
    print()
    print("TODO")


def test_package_id_exists():
    print("\nTESTING: Package ID exists")
    print()
    print("TODO")


def test_gen_new_package_id():
    print("\nTESTING: Generate new package ID")
    print()
    print("TODO")


def test_package_exists():
    print("\nTESTING: Package exists")
    print()
    print("TODO")


def test_execute_query():
    print("\nTESTING: Execute query")
    print()
    print("TODO")


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
