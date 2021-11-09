class Database():
    def __init__(self):
        # TODO make this resilient to missing environment variables
        # Initialize client
        self.client = bigquery.Client(project=os.environ["GOOGLE_CLOUD_PROJECT"])

        # Get dataset
        self.dataset = self.client.get_dataset(os.environ["BIGQUERY_DATASET"])

        # Get tables
        self.tables = self.client.list_tables(self.dataset)
    

    # Params: package: models/Package
    def upload_package(self, package):
        # Get package ID
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
