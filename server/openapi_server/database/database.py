class Database():
    def __init__(self):
        # TODO make this resilient to missing environment variables
        # Initialize client
        self.client = bigquery.Client(project=os.environ["GOOGLE_CLOUD_PROJECT"])

        # Get dataset
        self.dataset = self.client.get_dataset(os.environ["BIGQUERY_DATASET"])

        # Get tables
        self.tables = self.client.list_tables(self.dataset)
    

    # Params: 
    # user: models/User
    # package: models/Package
    def upload_package(self, user, package):
        # Get metadata and data
        metadata, data = package.metadata(), package.data()

        # Check if package already exists
        name = metadata.name()
        version = metadata.version()
        if self.package_exists(name, version):
            # TODO: Return error saying package already exists, use package update to change existing package
            return "some error"

        # Get id
        id = metadata.id()
        if id is None or self.id_exists("packages", id):
            # TODO: Include new id in response body
            id = self.gen_new_id("packages")
        
        # Content or URL or both should be set for upload
        content = data.content()
        url = data.url()
        if content is None and url is None:
            # TODO: Return error saying missing content or URL
            return "some error"

        # TODO: Implement sensitive and secret flags
        sensitive = False
        secret = True
        
        # Get js_program
        js_program = data.js_program()
        # TODO: Trigger separate query to insert js program first, then add the ID to the package upload

        # Get user id
        upload_user_id = user.id()

        # Generate query
        query = f"""
            INSERT INTO {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset}.packages (id, name, url, version, sensitive, secret, upload_user_id, zip)
            VALUES ({id}, "{name}", "{url}", "{version}", {sensitive}, {secret}, {upload_user_id}, "{content}")
        """

        results = self.execute_query(query)

        return None


    def gen_new_id(self, table):
        # TODO: Find lowest available positive integer ID in given table and return it
        return 5

    
    def id_exists(self, table, id):
        # Generate query
        query = f"""
            SELECT id from {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset}.{table} WHERE id = {id}
        """

        results = self.execute_query(query)
        # TODO: Check results to see if any records are returned
        return False

    
    def package_exists(self, name, version):
        # Generate query
        query = f"""
            SELECT name, version from {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset}.packages WHERE name = {name} AND version = {version}
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
