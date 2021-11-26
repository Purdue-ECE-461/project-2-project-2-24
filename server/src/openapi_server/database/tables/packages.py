import os
from openapi_server.models.error import Error

class Packages():
    def __init__(self, db):
        self.db = db

    def package_exists(self, name, version):
        # Generate query
        query = f"""
            SELECT name, version from {os.environ["GOOGLE_CLOUD_PROJECT"]}.{os.environ["BIGQUERY_DATASET"]}.packages 
            WHERE name = "{name}" AND version = "{version}"
        """

        results = self.db.execute_query(query)

        if isinstance(results, Error):
            return results
        else:
            return len(results) > 0
