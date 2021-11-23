from __future__ import absolute_import
from openapi_server.database import database
from openapi_server.models.package import Package
from openapi_server.models.package_data import PackageData
from openapi_server.models.package_metadata import PackageMetadata
from openapi_server.models.user import User
from dotenv import load_dotenv

load_dotenv()

db = database.Database()

user_group = None


def test_create_new_user(user):
    print("\nTESTING: Create new user")
    print()
    results = db.create_new_user(user, user, "password", 1)
    print("Created new user: ", results)


def test_create_new_token(auth_request):
    print("\nTESTING: Create new token")
    print()
    created_token = db.create_new_token(auth_request)
    print("New token: " + created_token)


def test_get_user_id_from_token(token):
    print("\nTESTING: Get user ID from token")
    print()
    user_id = db.get_user_id_from_token(token)
    print("User ID:", user_id)


def test_upload_package(token, package):
    print("\nTESTING: Upload package")
    print()
    metadata = db.upload_package(token=token, package=package)
    print("Uploaded metadata:", metadata)


def test_upload_js_program(package_id, js_program):
    print("\nTESTING: Upload js program")
    print()
    js_program_id = db.upload_js_program(package_id, js_program)
    print("JS program id:", js_program_id)


def test_gen_new_integer_id(table):
    print("\nTESTING: Generate new integer ID")
    print()
    new_id = db.gen_new_integer_id(table)
    print("New id:", new_id)


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


def test_package_id_exists(package_id):
    print("\nTESTING: Package ID exists")
    print()
    package_id_exists = db.package_id_exists(package_id)
    print("Package ID exists:", package_id_exists)


def test_package_exists(package):
    print("\nTESTING: Package exists")
    print()
    package_exists = db.package_exists(package.metadata.name, package.metadata.version)
    print("Package exists:", package_exists)


def test_execute_valid_query(valid_query):
    print("\nTESTING: Execute valid query")
    print()
    results = db.execute_query(valid_query)
    print("Execute valid query:", results)


def test_execute_invalid_query(invalid_query):
    print("\nTESTING: Execute invalid query")
    print()
    results = db.execute_query(invalid_query)
    print("Execute invalid query:", results)
