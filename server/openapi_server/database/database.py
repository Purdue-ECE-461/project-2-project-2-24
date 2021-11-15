from __future__ import absolute_import
from google.cloud import bigquery
from models import *
import os

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
    # user: models/User
    # package: models/Package
    def upload_package(self, user, package):
        # Get metadata and data
        metadata, data = package.metadata, package.data

        # Check if package already exists
        name = metadata.name
        version = metadata.version
        if self.package_exists(name, version):
            return Error(code=403, message="Package-Version already exists, use 'Update' instead!")

        # Get id
        id = metadata.id
        if id is None or self.id_exists("packages", id):
            # TODO: Include new id in response body
            id = self.gen_new_id("packages")
        
        # Content or URL or both should be set for upload
        content = data.content
        url = data.url
        if content is None and url is None:
            # TODO: Return error saying missing content or URL
            if content is None:
                return Error(code=400, message="Missing package content for upload!")
            else:
                return Error(code=400, message="Missing URL for ingest!")

        # Get user id
        #upload_user_id = self.get_user_id(user.name)'
        upload_user_id = 1

        # TODO: Implement sensitive and secret flags
        sensitive = False
        secret = True
        
        query = None
        if sensitive:
            # Get js_program
            js_program = data.js_program
            if js_program is not None:
                js_program_id = self.upload_js_program(id, js_program)
                # TODO: Trigger separate query to insert js program first, then add the ID to the package upload

            # Generate query
            query = f"""
                INSERT INTO {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.packages (id, name, url, version, sensitive, secret, upload_user_id, zip)
                VALUES ({id}, "{name}", "{url}", "{version}", {sensitive}, {secret}, {upload_user_id}, "{content}")
            """

        results = self.execute_query(query)

        return None


    def upload_js_program(self, package_id, js_program):
        # Get new script id
        id = self.gen_new_id("scripts")

        # Generate query
        query = f"""
            INSERT INTO {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.scripts (id, package_id, script)
            VALUES ({id}, {package_id}, "{js_program}")
        """

        # Execute query
        results = self.execute_query(query)

        return results


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
            FROM    {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.{table} to
            WHERE   NOT EXISTS
                    (
                    SELECT  NULL
                    FROM    {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.{table} ti 
                    WHERE   ti.id = to.id + 1
                    )
            ORDER BY
                    id
            LIMIT 1
        """

        # TODO: Parse results and return new id
        results = self.execute_query(query)

        new_id = results

        return new_id


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
            SELECT id from {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.users WHERE name = "{name}"
        """

        results = self.execute_query(query)
        # TODO: Get id from query, if it exists
        return 1

    
    def id_exists(self, table, id):
        # Generate query
        query = f"""
            SELECT id from {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.{table} WHERE id = {id}
        """

        results = self.execute_query(query)
        # TODO: Check results to see if any records are returned
        return False

    
    def package_exists(self, name, version):
        # Generate query
        query = f"""
            SELECT name, version from {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.packages WHERE name = "{name}" AND version = "{version}"
        """

        results = self.execute_query(query)

        # TODO: Check results to see if any records are returned
        return False


    def execute_query(self, query):
        query_job = self.client.query(query)

        print("QUERY RESPONSE:")
        for row in query_job:
            print(row)

        return query_job
