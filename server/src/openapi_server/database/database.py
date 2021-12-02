from __future__ import absolute_import

import datetime
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
from openapi_server.models.user import User
from openapi_server.models.user_authentication_info import UserAuthenticationInfo
from openapi_server.models.user_group import UserGroup

from openapi_server.database import utils

import os
import hashlib
import time

# TODO: REFACTOR AND REFORMAT QUERIES SO THAT UPLOAD PACKAGE ONLY REQUIRES ONE COMBINED QUERY

PACKAGE_PAGE_SIZE = 10
MAX_TOKEN_USES = 1000
MAX_TOKEN_AGE = 10


class Database:
    def __init__(self):
        # Initialize client
        try:
            self.client = bigquery.Client(project=os.environ["GOOGLE_CLOUD_PROJECT"])

            # Get dataset
            self.dataset = self.client.get_dataset(os.environ["BIGQUERY_DATASET"])

            # Get tables
            self.tables = self.client.list_tables(self.dataset)

            # Ensure proper initial state
            results = self.initialize()
            if isinstance(results, Error):
                raise KeyError(results.message)

        except KeyError as err:
            print("Cannot initialize Database!!!")
            print(err)

    # ________________________________________________________________________________________________________________
    #                                                   HISTORY
    # ________________________________________________________________________________________________________________

    # ________________________________________________________________________________________________________________
    #                                                   PACKAGES
    # ________________________________________________________________________________________________________________

    def update_package(self, user, package_id, package):
        # Get metadata and data
        metadata, data = package.metadata, package.data

        # Name, version, and ID must match
        name = metadata.name
        version = metadata.version
        existing_package_id = self.get_package_id(name, version)
        if isinstance(existing_package_id, Error):
            return existing_package_id
        elif existing_package_id != package_id:
            return Error(code=403, message="Supplied ID (" + package_id + ") does not match ID in registry (" + existing_package_id + ")!")
        metadata.id = package_id

        # Update is only for content
        content = data.content
        if content is None:
            return Error(code=400, message="Missing Content for package update!")

        # Get user id
        upload_user_id = user.id
        if upload_user_id is None:
            return Error(code=500, message="Could not find ID of uploading user!!")

        # Generate query
        query = f"""
                    UPDATE {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.packages 
                    SET upload_user_id = {upload_user_id}, zip = "{content}"
                    WHERE id = "{metadata.id}"
                """

        results = self.execute_query(query)

        if isinstance(results, Error):
            return results
        else:
            return {"description": "Success."}

    # Params:
    # auth: token (string)
    # package: package (models/Package)
    def upload_package(self, user, package):
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

        # Get user id
        upload_user_id = user.id
        if upload_user_id is None:
            return Error(code=500, message="Cannot find ID of uploading user!!")

        # TODO: Implement sensitive and secret flags
        sensitive = metadata.sensitive if metadata.sensitive is not None else False
        secret = metadata.secret if metadata.secret is not None else False

        if sensitive:
            # Get js_program
            js_program = data.js_program
            if js_program is not None:
                js_result = self.upload_js_program(package_id, js_program)
                if isinstance(js_result, Error):
                    return js_result

        # Content provided for package upload, URL provided for package ingest
        content = data.content
        url = data.url
        if content is None and url is not None:
            # Ingest package query
            # TODO: MUST RATE FIRST -> if net score greater than 0.5, then it is "ingestible" and gets added
            query = f"""
                                    INSERT INTO {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.packages (id, name, url, version, sensitive, secret, upload_user_id, zip)
                                    VALUES ("{package_id}", "{name}", "{url}", "{version}", {sensitive}, {secret}, {upload_user_id}, NULL)
                                """
        elif content is not None and url is None:
            # Upload package query
            query = f"""
                        INSERT INTO {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.packages (id, name, url, version, sensitive, secret, upload_user_id, zip)
                        VALUES ("{package_id}", "{name}", NULL, "{version}", {sensitive}, {secret}, {upload_user_id}, "{content}")
                    """
        elif content is not None and url is not None:
            return Error(code=400, message="Cannot provide both Content and URL in the same request!")
        else:
            # Both are not provided
            return Error(code=400, message="Missing URL or Content!")

        results = self.execute_query(query)

        if isinstance(results, Error):
            return results
        else:
            return metadata

    def package_id_exists(self, package_id):
        # Generate query
        query = f"""
            SELECT id from {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.packages WHERE id = "{package_id}"
        """

        results = self.execute_query(query)

        if isinstance(results, Error):
            return results
        else:
            return len(results) > 0

    def package_exists(self, name, version):
        # Generate query
        query = f"""
            SELECT name, version from {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.packages WHERE name = "{name}" AND version = "{version}"
        """

        results = self.execute_query(query)

        if isinstance(results, Error):
            return results
        else:
            return len(results) > 0

    def get_package_id(self, name, version):
        # Generate query
        query = f"""
            SELECT id, name, version from {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.packages WHERE name = "{name}" AND version = "{version}"
        """

        results = self.execute_query(query)

        if isinstance(results, Error):
            return results
        elif len(results) > 0:
            return results[0]["id"]
        else:
            return Error(code=400, message="Could not find provided package!")

    # TODO: Support package_query name and version parameters
    # For now, this ignores what is specified in package_query
    def get_page_of_packages(self, user, package_query, offset):
        # If no offset provided, get first page
        if offset is None or offset == "":
            offset = 0
        else:
            try:
                offset = int(offset)
            except ValueError:
                return Error(code=400, message="Provided offset is invalid (not a number)!")

        # Download requested rows
        table = self.client.get_table(f'{os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.packages')
        fields = [table.schema[0], table.schema[1], table.schema[3]]
        requested_rows = list(self.client.list_rows(
            table=table,
            selected_fields=fields,
            start_index=(offset * PACKAGE_PAGE_SIZE),
            page_size=PACKAGE_PAGE_SIZE
        ))

        output = []
        for row in requested_rows:
            output.append({
                "Name": row["name"],
                "Version": row["version"],
                "ID": row["id"]
            })

        return output

    # ________________________________________________________________________________________________________________
    #                                                   RATINGS
    # ________________________________________________________________________________________________________________

    # ________________________________________________________________________________________________________________
    #                                                   SCRIPTS
    # ________________________________________________________________________________________________________________

    def upload_js_program(self, package_id, js_program):
        # Get new script id
        js_program_id = self.gen_new_integer_id("scripts")
        if isinstance(js_program_id, Error):
            return js_program_id

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

    # ________________________________________________________________________________________________________________
    #                                                   TOKENS
    # ________________________________________________________________________________________________________________

    def create_new_token(self, auth_request):
        # First get id of user
        user_id = self.get_user_id(auth_request.user.name)
        if user_id is None:
            return Error(code=500, message="Could not find User ID of provided User!")

        # Then check user's password
        if not self.user_password_is_correct(auth_request, user_id):
            return Error(code=401, message="Incorrect password provided!")

        new_token_id = self.gen_new_integer_id("tokens")
        new_token = utils.db_hash(str(round(time.time() * 1000)))
        new_token_hash = utils.db_hash(new_token)

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
        hashed_token = utils.db_hash(token)

        query = f"""
            SELECT user_id FROM {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.tokens WHERE hash_token = "{hashed_token}"
        """

        results = self.execute_query(query)

        if isinstance(results, Error):
            return results
        elif len(results) > 0:
            return results[0].get("user_id", default=None)
        else:
            return Error(code=400, message="Provided token not recognized!")

    def get_user_from_token(self, token):
        # Hash token
        hashed_token = utils.db_hash(token)

        user_query = f"""
            WITH user_id_query AS (
                SELECT user_id FROM {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.tokens
                WHERE hash_token = "{hashed_token}"
            )
            
            SELECT user_id_query.user_id, users.id, users.username, users.hash_pass, users.user_group_id,
            user_groups.id, user_groups.name as user_group_name, user_groups.upload, user_groups.search, user_groups.download, user_groups.create_user
            FROM user_id_query, {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.users users, {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.user_groups user_groups
            WHERE users.id = user_id_query.user_id AND user_groups.id = users.user_group_id;
        """

        user_query_results = self.execute_query(user_query)
        if isinstance(user_query_results, Error):
            return user_query_results
        elif len(user_query_results) == 1:
            user_query_row = user_query_results[0]
            user_group = UserGroup(
                id=user_query_row["user_group_id"],
                name=user_query_row["user_group_name"],
                upload=user_query_row["upload"],
                search=user_query_row["search"],
                download=user_query_row["download"],
                create_user=user_query_row["create_user"]
            )
            user = User(
                id=user_query_row["user_id"],
                name=user_query_row["username"],
                is_admin=(user_query_row["user_group_id"] == 1),
                user_authentication_info=UserAuthenticationInfo(password=user_query_row["hash_pass"]),
                user_group=user_group
            )
            return user
        else:
            return Error(code=500, message="Could not find owner of token!")

    def check_token_expiration(self, token):
        # Generate query
        query = f"""
            SELECT id, hash_token, created, interactions, user_id FROM {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.tokens
            WHERE hash_token = "{utils.db_hash(token)}"
        """

        results = self.execute_query(query)

        if isinstance(results, Error):
            return results

        if len(results) > 0:
            token_details = results[0]
        else:
            return Error(code=401, message="Provided token not recognized!")

        # Check if token is more than MAX_TOKEN_AGE hours old
        current_time = datetime.datetime.now(datetime.timezone.utc)
        token_expiration = token_details["created"] + datetime.timedelta(hours=MAX_TOKEN_AGE)
        if current_time > token_expiration:
            return Error(code=401, message="Token expired: more than " + str(MAX_TOKEN_AGE) + " hours old!")

        # Now check if token has been used more than MAX_TOKEN_USES times
        remaining_uses = token_details["interactions"]
        if remaining_uses < 1:
            return Error(code=401, message="Token expired: used more than " + str(MAX_TOKEN_USES) + " times!")

        # Token is valid
        return {"message": "Token is valid!"}

    def decrement_token_interactions(self, token):
        # Generate query
        query = f"""
            UPDATE {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.tokens
            SET interactions = interactions - 1
            WHERE hash_token = "{utils.db_hash(token)}"
        """

        return self.execute_query(query)

    # ________________________________________________________________________________________________________________
    #                                                USER GROUPS
    # ________________________________________________________________________________________________________________

    def create_new_user_group(self, token, user_group):
        # TODO FINISH THIS FUNCTION
        # TODO MOVE PERMISSION CHECK TO DEFAULT API FILE
        # Is user allowed to create a new UserGroup?
        user = self.get
        if not user.is_admin:
            return Error(code=401, message="Must be admin to create new user")

        # Generate id for new user
        new_user_id = self.gen_new_integer_id("users")

        # Get username
        new_user_username = new_user.name

        # Get password
        new_user_password_hash = utils.db_hash(password)

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

    def get_user_group_id(self, group_name):
        # Generate query
        query = f"""
            SELECT id from {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.user_groups WHERE name = "{group_name}"
        """
        results = self.execute_query(query)

        if isinstance(results, Error):
            return results
        elif len(results) > 0:
            return int(results[0].get("id", default="1"))
        else:
            return Error(code=400, message="Could not find user group with provided name!")

    # ________________________________________________________________________________________________________________
    #                                                   USERS
    # ________________________________________________________________________________________________________________

    def create_new_user(self, user, new_user, password, user_group_name):
        # Is user allowed to create a new user?
        if not user.is_admin:
            return Error(code=401, message="Must be admin to create new user")

        # Generate id for new user
        new_user_id = self.gen_new_integer_id("users")

        # Get username
        new_user_username = new_user.name

        # Get password
        new_user_password_hash = utils.db_hash(password)

        # Get user group id
        user_group_id = self.get_user_group_id(user_group_name)
        if isinstance(user_group_id, Error):
            return user_group_id

        # Generate query
        query = f"""
            INSERT INTO {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.users (id, username, hash_pass, user_group_id)
            VALUES ({new_user_id}, "{new_user_username}", "{new_user_password_hash}", {user_group_id})
        """

        results = self.execute_query(query)

        return results

    def get_user_id(self, name):
        # Generate query
        query = f"""
            SELECT id FROM {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.users WHERE username = "{name}"
        """

        results = self.execute_query(query)

        if isinstance(results, Error):
            return results
        elif len(results) > 0:
            return int(results[0].get("id", default="1"))
        else:
            return Error(code=400, message="Could not find user with provided name!")

    def user_password_is_correct(self, auth_request, user_id):
        # Get hash of provided password
        given_password_hash = utils.db_hash(auth_request.secret.password)

        # Get hash of user's actual password
        query = f"""
            SELECT id, hash_pass FROM {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.users
            WHERE id = {user_id}
        """

        results = self.execute_query(query)
        if isinstance(results, Error):
            return results
        elif len(results) > 0:
            user_password_hash = results[0]["hash_pass"]
            return user_password_hash == given_password_hash
        else:
            return Error(code=400, message="Could not find given user!")

    # ________________________________________________________________________________________________________________
    #                                                   COMMON
    # ________________________________________________________________________________________________________________

    def initialize(self):
        # Initialize query
        query = f""

        # First add default user group
        query += f"""
                    INSERT INTO ece-461-proj-2-24.module_registry.user_groups (id, name, upload, search, download, create_user)
                    SELECT new_id, new_Name, new_upload, new_search, new_download, new_create_user FROM (SELECT 1 AS new_id, "Admins" AS new_name, TRUE AS new_upload, TRUE AS new_search, TRUE AS new_download, TRUE AS new_create_user)
                    LEFT JOIN ece-461-proj-2-24.module_registry.user_groups
                    ON id = new_id
                    WHERE id IS NULL;
                """

        # Add default user
        query += f"""
                    INSERT INTO {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.users (id, username, hash_pass, user_group_id)
                    SELECT new_id, new_username, new_hash_pass, new_user_group_id FROM (SELECT 1 AS new_id, "ece461defaultadminuser" AS new_username, "{utils.db_hash("correcthorsebatterystaple123(!__+@**(A")}" AS new_hash_pass, 1 AS new_user_group_id)
                    LEFT JOIN {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.users
                    ON id = new_id
                    WHERE id IS NULL;
                """

        # Add default token (for testing)
        query += f"""
                    INSERT INTO {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.tokens (id, hash_token, created, interactions, user_id)
                    SELECT new_id, new_hash_token, new_created, new_interactions, new_user_id FROM (SELECT 1 AS new_id, "{utils.db_hash("default_token")}" AS new_hash_token, CURRENT_TIMESTAMP() AS new_created, {MAX_TOKEN_USES} AS new_interactions, 1 AS new_user_id)
                    LEFT JOIN {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.tokens
                    ON id = new_id
                    WHERE id IS NULL;
                """

        # Execute query
        return self.execute_query(query)

    def reset_registry(self):
        # First clear all tables
        query = f"""
            DELETE FROM {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.history WHERE TRUE;
            DELETE FROM {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.packages WHERE TRUE;
            DELETE FROM {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.ratings WHERE TRUE;
            DELETE FROM {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.scripts WHERE TRUE;
            DELETE FROM {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.tokens WHERE TRUE;
            DELETE FROM {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.user_groups WHERE TRUE;
            DELETE FROM {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.users WHERE TRUE;
        """

        results = self.execute_query(query)

        if isinstance(results, Error):
            return results

        # Now initialize the database
        results = self.initialize()

        if isinstance(results, Error):
            return results
        else:
            return {"message": "Successfully reset registry!"}

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
            return int(results[0].get("new_id", default="1"))

    def gen_new_uuid(self):
        # Generate query
        query = f"""
            SELECT GENERATE_UUID() AS new_uuid
        """

        results = self.execute_query(query)

        if isinstance(results, Error):
            return results
        elif len(results) > 0:
            return results[0].get("new_uuid")
        else:
            return Error(code=500, message="Could not generate new UUID!")

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
