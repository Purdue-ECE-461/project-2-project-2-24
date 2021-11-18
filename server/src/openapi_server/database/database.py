from __future__ import absolute_import
from re import L
from google.cloud import bigquery
from openapi_server.models.extra_models import TokenModel  # noqa: F401
from openapi_server.models.authentication_request import AuthenticationRequest
from openapi_server.models.error import Error
from openapi_server.models.package import Package
from openapi_server.models.package_history_entry import PackageHistoryEntry
from openapi_server.models.package_metadata import PackageMetadata
from openapi_server.models.package_query import PackageQuery
from openapi_server.models.package_rating import PackageRating
import os

# TODO: REFACTOR AND REFORMAT QUERIES SO THAT UPLOAD PACKAGE ONLY REQUIRES ONE COMBINED QUERY

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
            exit(1)


    # Params: 
    # auth: token (string)
    # package: package (models/Package)
    def upload_package(self, auth, package):
        # Initialize query
        query = ""

        # Get metadata and data
        metadata, data = package.metadata, package.data

        # Add check if package already exists
        name = metadata.name
        version = metadata.version
        if self.package_exists(name, version):
            return Error(code=403, message="Package-Version already exists, use 'Update' instead!")

        # Get id
        id = metadata.id
        if id is None or self.id_exists("packages", id):
            id = self.gen_new_id("packages")
            metadata.id = id
        
        # Content or URL or both should be set for upload
        content = data.content
        url = data.url
        if content is None and url is None:
            if content is None:
                return Error(code=400, message="Missing package content for upload!")
            else:
                return Error(code=400, message="Missing URL for ingest!")

        # Get user id
        upload_user_id = self.get_user_id_from_token(token)
        # TODO: CHECK AND REMOVE THIS
        upload_user_id=7
        if upload_user_id is None:
            return Error(code=500, message="Cannot find ID of uploading user!!")

        # TODO: Implement sensitive and secret flags
        sensitive = True
        secret = True
        
        query = None
        if sensitive:
            # Get js_program
            js_program = data.js_program
            if js_program is not None:
                self.upload_js_program(id, js_program)

        # Generate query
        query = f"""
            INSERT INTO {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.packages (id, name, url, version, sensitive, secret, upload_user_id, zip)
            VALUES ({id}, "{name}", "{url}", "{version}", {sensitive}, {secret}, {upload_user_id}, "{content}")
        """

        results = self.execute_query(query)
        
        # TODO: Ensure upload was successful.  If it was, return metadata, if not, return an error

        return metadata


    def upload_js_program(self, package_id, js_program):
        # Get new script id
        id = self.gen_new_id("scripts")

        # Generate query
        query = f"""
            INSERT INTO {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.scripts (id, package_id, script)
            VALUES ({id}, {package_id}, "{js_program.encode("unicode_escape").decode("utf-8")}")
        """

        # Execute query
        results = self.execute_query(query)

        return id


    def create_new_user(self, user, new_user, password, user_group):
        # Is user allowed to create a new user?
        if (not user.is_admin):
            # TODO: Return error here that user is not allowed to make new users
            return 0
        
        # Generate id for new user
        new_user_id = self.gen_new_id("users")

        # Get user group id
        user_group_id = self.get_user_group_id(user_group)

        # Generate query
        query = f"""
            INSERT INTO {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.users (id, name, url, version, sensitive, secret, upload_user_id, zip)
            VALUES ({id}, "{name}", "{url}", "{version}", {sensitive}, {secret}, {upload_user_id}, "{content}")
        """

        results = self.execute_query(query)

        return results


    def gen_new_id(self, table):
        # TODO: Find lowest available positive integer ID in given table and return it
        query = f"""
            SELECT  id + 1
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

        # TODO: Parse results and return new id
        results = self.execute_query(query)

        if (len(results) == 0):
            return 1
        else:
            # TODO CHECK THIS
            #return results[0].get("id")
            # TODO FIX THIS
            return 8


    def get_user_group_id(self, group_name):
        # Generate query
        query = f"""
            SELECT id from {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.user_groups WHERE name = "{group_name}"
        """
        results = self.execute_query(query)
        # TODO: Get id from query, if it exists
        return 1

    
    def get_user_id(self, name):
        # Generate query
        query = f"""
            SELECT id from {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.users WHERE username = "{name}"
        """

        results = self.execute_query(query)

        if (len(results) > 0):
            return results[0].get("id")
        else:
            return None

    
    def id_exists(self, table, id):
        # Generate query
        query = f"""
            SELECT id from {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.{table} WHERE id = {id}
        """

        results = self.execute_query(query)

        return (len(results) > 0)

    
    def package_exists(self, name, version):
        # Generate query
        query = f"""
            SELECT name, version from {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.packages WHERE name = "{name}" AND version = "{version}"
        """

        results = self.execute_query(query)

        return (len(results) > 0)


    def execute_query(self, query):
        print("QUERY:")
        print(query)
        query_job = self.client.query(query)

        results = list(query_job.result())

        print("QUERY RESPONSE:")
        for row in results:
            print(row)

        return results
