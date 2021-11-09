from google.cloud import bigquery

class Database():
    def __init__(self):
        # Initialize client
        self.client = bigquery.Client(project="ece-461-proj-2-24")

    def test_query(self):
        query = """
        INSERT INTO ece-461-proj-2-24.module_registry.packages (id, name, url, version, sensitive, secret, upload_user_id, zip)
        VALUES (1, "sample", "https://www.sample.com", "1.0.0", false, false, 1, "base64encodedpackage")
        """
        query_job = self.client.query(query)  # Make an API request.

        print("The query response:")
        print(query_job)
        for row in query_job:
            # Row values can be accessed by field name or index.
            print(row)

        return None