from __future__ import absolute_import
from re import L
from google.cloud import bigquery
from google.api_core.exceptions import BadRequest
from openapi_server.models.extra_models import TokenModel  # noqa: F401
from openapi_server.models.authentication_request import AuthenticationRequest
from openapi_server.models.error import Error
from openapi_server.models.package import Package
from openapi_server.models.package_history_entry import PackageHistoryEntry
from openapi_server.models.package_metadata import PackageMetadata
from openapi_server.models.package_query import PackageQuery
from openapi_server.models.package_rating import PackageRating
from openapi_server.database.tables import *
import os
import hashlib
import time


# TODO: REFACTOR AND REFORMAT QUERIES SO THAT UPLOAD PACKAGE ONLY REQUIRES ONE COMBINED QUERY

MAX_TOKEN_USES = 1000

class Database():
    def __init__(self):
        # Initialize client
        try:
            self.client = bigquery.Client(project=os.environ["GOOGLE_CLOUD_PROJECT"])

            # Get dataset
            self.dataset = self.client.get_dataset(os.environ["BIGQUERY_DATASET"])

            # Get tables
            self.tables = self.client.list_tables(self.dataset)
        except KeyError as err:
            print("Cannot initialize Database!!!")
            print(err)

    def hash(self, content):
        return hashlib.sha256(content.encode()).hexdigest()

    def create_new_token(self, auth_request):
        # TODO: Confirm user password is valid

        user_id = self.get_user_id(auth_request.user.name)
        new_token_id = self.gen_new_integer_id("tokens")
        new_token = self.hash(str(round(time.time() * 1000)))
        new_token_hash = self.hash(new_token)

        query = f"""
            INSERT INTO {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.tokens (id, hash_token, created, interactions, user_id)
            VALUES ({new_token_id}, "{new_token_hash}", CURRENT_TIMESTAMP(), {MAX_TOKEN_USES}, {user_id})
        """

        results = self.execute_query(query)

        if isinstance(results, Error):
            return results
        else:
            return new_token

    def get_user_id_from_token(self, token):
        hashed_token = self.hash(token)

        query = f"""
            SELECT user_id FROM {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.tokens WHERE hash_token = "{hashed_token}"
        """

        results = self.execute_query(query)

        if isinstance(results, Error):
            return results
        elif len(results) > 0:
            return results[0].get("user_id", default=None)
        else:
            return None

    # Params:
    # auth: token (string)
    # package: package (models/Package)
    def upload_package(self, token, package):
        # Get metadata and data
        metadata, data = package.metadata, package.data

        # Add check if package already exists
        # TODO: * character is reserved
        name = metadata.name
        version = metadata.version
        if self.package_exists(name, version):
            return Error(code=403, message="Package-Version already exists, use 'Update' instead!")

        # Get id
        package_id = metadata.id
        if package_id is None:
            package_id = name + "_" + version
        elif self.package_id_exists(package_id):
            package_id = package_id + "_" + name + "_" + version
        metadata.id = package_id

        # Content or URL or both should be set for upload
        content = data.content
        url = data.url
        if content is None and url is None:
            if content is None:
                return Error(code=400, message="Missing package contents for upload!")
            else:
                return Error(code=400, message="Missing URL for ingest!")

        # Get user id
        upload_user_id = self.get_user_id_from_token(token)
        if upload_user_id is None:
            return Error(code=500, message="Cannot find ID of uploading user!!")

        # TODO: Implement sensitive and secret flags
        # Do this by adding these flags to Project metadata?
        # While you're add it, add user group to user model (in yaml spec)
        # Maybe add UserGroup model as well?
        # While you're add it, add any other models needed
        # See if we're allowed to change the spec first
        sensitive = True
        secret = True

        if sensitive:
            # Get js_program
            js_program = data.js_program
            if js_program is not None:
                self.upload_js_program(package_id, js_program)

        # Generate query
        query = f"""
            INSERT INTO {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.packages (id, name, url, version, sensitive, secret, upload_user_id, zip)
            VALUES ("{package_id}", "{name}", "{url}", "{version}", {sensitive}, {secret}, {upload_user_id}, "{content}")
        """

        results = self.execute_query(query)

        if isinstance(results, Error):
            return results
        else:
            return metadata

    def upload_js_program(self, package_id, js_program):
        # Get new script id
        js_program_id = self.gen_new_integer_id("scripts")
        if js_program_id is None:
            return Error(code=500, message="Couldn't generate new js_program id!")

        # Generate query
        query = f"""
            INSERT INTO {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.scripts (id, package_id, script)
            VALUES ({js_program_id}, "{package_id}", "{js_program.encode("unicode_escape").decode("utf-8")}")
        """

        # Execute query
        results = self.execute_query(query)

        if isinstance(results, Error):
            return results
        else:
            return js_program_id

    def create_new_user(self, user, new_user, password, user_group):
        # Is user allowed to create a new user?
        if not user.is_admin:
            return Error(code=401, message="Must be admin to create new user")

        # Generate id for new user
        new_user_id = self.gen_new_integer_id("users")

        # Get username
        new_user_username = new_user.name

        # Get password
        new_user_password_hash = self.hash(password)

        # Get user group id
        user_group_id = self.get_user_group_id(user_group)
        if user_group_id is None:
            return Error(code=400, message="Cannot find user group with provided name! User not created!")

        # Generate query
        query = f"""
            INSERT INTO {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.users (id, username, hash_pass, user_group_id)
            VALUES ({new_user_id}, "{new_user_username}", "{new_user_password_hash}", "{user_group_id}")
        """

        results = self.execute_query(query)

        return results

    def create_new_user_group(self, token, user_group):
        # Is user allowed to create a new user?
        if not user.is_admin:
            return Error(code=401, message="Must be admin to create new user")

        # Generate id for new user
        new_user_id = self.gen_new_integer_id("users")

        # Get username
        new_user_username = new_user.name

        # Get password
        new_user_password_hash = self.hash(password)

        # Get user group id
        user_group_id = self.get_user_group_id(user_group)
        if user_group_id is None:
            return Error(code=400, message="Cannot find user group with provided name! User not created!")

        # Generate query
        query = f"""
                    INSERT INTO {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.users (id, username, hash_pass, user_group_id)
                    VALUES ({new_user_id}, "{new_user_username}", "{new_user_password_hash}", "{user_group_id}")
                """

        results = self.execute_query(query)

        return results
        return

    def gen_new_integer_id(self, table):
        query = f"""
            SELECT  id + 1 AS new_id
            FROM    {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.{table} tableo
            WHERE   NOT EXISTS
                    (
                    SELECT  NULL
                    FROM    {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.{table} tablei 
                    WHERE   tablei.id = tableo.id + 1
                    )
            ORDER BY
                    id
            LIMIT 1
        """

        results = self.execute_query(query)

        if isinstance(results, Error):
            return results
        elif len(results) == 0:
            return 1
        else:
            return results[0].get("new_id", default=None)

    def get_user_group_id(self, group_name):
        # Generate query
        query = f"""
            SELECT id from {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.user_groups WHERE name = "{group_name}"
        """
        results = self.execute_query(query)

        if isinstance(results, Error):
            return results
        elif len(results) == 0:
            return None
        else:
            return results[0].get("id", default=None)

    def get_user_id(self, name):
        # Generate query
        query = f"""
            SELECT id from {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.users WHERE username = "{name}"
        """

        results = self.execute_query(query)

        if isinstance(results, Error):
            return results
        elif len(results) == 0:
            return None
        else:
            return results[0].get("id", default=None)

    def package_id_exists(self, id):
        # Generate query
        query = f"""
            SELECT id from {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.packages WHERE id = "{id}"
        """

        results = self.execute_query(query)

        if isinstance(results, Error):
            return results
        else:
            return (len(results) > 0)

    def gen_new_uuid(self):
        # Generate query
        query = f"""
            SELECT GENERATE_UUID() AS new_uuid
        """

        results = self.execute_query(query)

        if isinstance(results, Error):
            return results
        elif len(results) == 0:
            return None
        else:
            return results[0].get("new_uuid")

    def package_exists(self, name, version):
        # Generate query
        query = f"""
            SELECT name, version from {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.packages WHERE name = "{name}" AND version = "{version}"
        """

        results = self.execute_query(query)

        if isinstance(results, Error):
            return results
        else:
            return (len(results) > 0)

    def execute_query(self, query):
        print("QUERY:")
        print(query)

        query_job = self.client.query(query)

        try:
            results = list(query_job.result())
            print("QUERY RESPONSE:")
            for row in results:
                print(row)
            return results

        except BadRequest as e:
            error_output = ""
            for e in query_job.errors:
                error_output += 'ERROR: {}'.format(e['message']) + "\n"
            print(error_output)
            return Error(code=500, message=error_output)
