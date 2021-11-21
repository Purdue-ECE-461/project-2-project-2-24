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
user_group = None

valid_query = f"""
    SELECT COUNT(*) FROM `ece-461-proj-2-24.module_registry.packages`
"""

invalid_query = f"""
    SELECT invalid_something FROM `table.smmethin.packages`
"""


def test_create_new_token():
    print("\nTESTING: Create new token")
    print()
    new_token = db.create_new_token(1)
    print("New token: " + new_token)
    return new_token


def test_get_user_id_from_token(token):
    print("\nTESTING: Get user ID from token")
    print()
    user_id = db.get_user_id_from_token(token)
    print("User ID:", user_id)
    return user_id


def test_upload_package(new_package):
    print("\nTESTING: Upload package")
    print()
    metadata = db.upload_package(token="example_token", package=new_package)
    print("Uploaded metadata:", metadata)
    return metadata


def test_upload_js_program(package_id, js_program):
    print("\nTESTING: Upload js program")
    print()
    js_program_id = db.upload_js_program(package_id, js_program)
    print("JS program id:", js_program_id)
    return js_program_id


def test_create_new_user(user, new_user):
    print("\nTESTING: Create new user")
    print()
    results = db.create_new_user(user, new_user, "password", 1)
    print("Created new user: ", results)
    return results


def test_gen_new_integer_id(table):
    print("\nTESTING: Generate new integer ID")
    print()
    new_id = db.gen_new_integer_id(table)
    print("New id:", new_id)
    return new_id


# def test_create_new_user_group():
#     print("\nTESTING: Create new user group")
#     print()
#     new_group = db.create_new_user_group(user_group)
#     print("New user group:", new_group)
#     return new_group
#
#
# def test_get_user_group_id():
#     print("\nTESTING: Get user group ID")
#     print()
#     print("TODO")


def test_get_user_id(username):
    print("\nTESTING: Get user ID")
    print()
    user_id = db.get_user_id(username)
    print("User id:", user_id)
    return user_id


def test_package_id_exists(package_id):
    print("\nTESTING: Package ID exists")
    print()
    package_id_exists = db.package_id_exists(package_id)
    print("Package ID exists:", package_id_exists)
    return package_id_exists


def test_package_exists(package_name, package_version):
    print("\nTESTING: Package exists")
    print()
    package_exists = db.package_exists(package_name, package_version)
    print("Package exists:", package_exists)
    return package_exists


def test_execute_query(query):
    print("\nTESTING: Execute query")
    print()
    results = db.execute_query(query)
    print("Execute query:", results)
    return results


if __name__ == "__main__":
    new_integer_id = test_gen_new_integer_id("users")
    test_create_new_user(user, new_user)
    new_token = test_create_new_token()
    user_id = test_get_user_id_from_token(new_token)
    metadata = test_upload_package(package)
    test_upload_js_program(metadata.id, package.data.js_program)
    user_id = test_get_user_id(user.name)
    package_id_exists = test_package_id_exists("package_id")
    package_exists = test_package_exists(package.metadata.name, package.metadata.version)
    test_execute_query(valid_query)
    test_execute_query(invalid_query)
    # user_group = test_create_new_user_group()
    # user_group_id = test_get_user_group_id(user_group.name)
