from __future__ import absolute_import
from openapi_server.database import database
from openapi_server.models.error import Error
from openapi_server.models.package_metadata import PackageMetadata
from dotenv import load_dotenv

load_dotenv()

db = database.Database()


def test_reset_registry(default_token):
    print("\nTESTING: Reset registry")
    print()
    result = db.reset_registry(default_token)
    print("Reset result:", result)
    assert not isinstance(result, Error)


def test_create_new_user_group(default_token, admin_user_group):
    print("\nTESTING: Create new user group")
    print()
    new_group = db.create_new_user_group(default_token, admin_user_group)
    print("New user group:", new_group)
    assert not isinstance(new_group, Error)


def test_get_user_group_id():
    print("\nTESTING: Get user group ID")
    print()
    print("TODO")


def test_create_new_user(default_user, new_user, new_user_password, admin_user_group_name):
    print("\nTESTING: Create new user")
    print()
    results = db.create_new_user(default_user, new_user, new_user_password, admin_user_group_name)
    print("Created new user:", results)
    assert not isinstance(results, Error)


def test_create_new_token(default_auth_request):
    print("\nTESTING: Create new token")
    print()
    created_token = db.create_new_token(default_auth_request)
    print("New token:", created_token)
    assert isinstance(created_token, str)


def test_get_user_id_from_token(default_token):
    print("\nTESTING: Get user ID from token")
    print()
    user_id = db.get_user_id_from_token(default_token)
    print("User ID:", user_id)
    assert isinstance(user_id, int)


def test_upload_package(default_user, package):
    print("\nTESTING: Upload package")
    print()
    metadata = db.upload_package(user=default_user, package=package)
    print("Uploaded metadata:", metadata)
    assert isinstance(metadata, PackageMetadata)
    

def test_download_package(default_user, package_id):
    print("\nTESTING: Download package")
    print()
    package = db.download_package(user=default_user, package_id=package_id)
    print("Downloaded Package:", package)
    assert isinstance(package, Package)


def test_update_package(default_token, package_id, package):
    print("\nTESTING: Update package")
    print()
    metadata = db.update_package(token=default_token, package_id=package_id, package=package)
    print("Updated metadata:", metadata)
    assert isinstance(metadata, PackageMetadata)


def test_upload_js_program(package_id, js_program):
    print("\nTESTING: Upload js program")
    print()
    js_program_id = db.upload_js_program(package_id, js_program)
    print("JS program id:", js_program_id)
    assert isinstance(js_program_id, int)


def test_gen_new_integer_id(table):
    print("\nTESTING: Generate new integer ID")
    print()
    new_id = db.gen_new_integer_id(table)
    print("New id:", new_id)
    assert isinstance(new_id, int)


def test_get_user_id(default_username):
    print("\nTESTING: Get user ID")
    print()
    user_id = db.get_user_id(default_username)
    print("User id:", user_id)
    assert isinstance(user_id, int)


def test_package_id_exists(package_id):
    print("\nTESTING: Package ID exists")
    print()
    package_id_exists = db.package_id_exists(package_id)
    print("Package ID exists:", package_id_exists)
    assert isinstance(package_id_exists, bool)


def test_package_exists(package):
    print("\nTESTING: Package exists")
    print()
    package_exists = db.package_exists(package.metadata.name, package.metadata.version)
    print("Package exists:", package_exists)
    assert isinstance(package_exists, bool)


def test_execute_valid_query(valid_query):
    print("\nTESTING: Execute valid query")
    print()
    results = db.execute_query(valid_query)
    print("Execute valid query:", results)
    assert not isinstance(results, Error)


def test_execute_invalid_query(invalid_query):
    print("\nTESTING: Execute invalid query")
    print()
    results = db.execute_query(invalid_query)
    print("Execute invalid query:", results)
    assert isinstance(results, Error)
