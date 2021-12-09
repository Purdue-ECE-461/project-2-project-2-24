# project-2-project-2-24

# About the program
Our system is an API which is connected to a backend server.  The API can receive requests to upload, update, download, and rate individual packages. 

The API itself is hosted in Google Cloud Platform (GCP) App Engine, and the database is hosted in GCP BigQuery.  

Users can interact with the API like any other API, using Postman, cURL, a custom script, within their application, or through any other interface.  

Admins can register users, who can then request access tokens using their personal login information.  

Packages can be uploaded via base64 encoded string of the .zip contents, or ingested via URL.  Downloaded packages are provided in base64 form.

# How to run server

Change directory to the "server" directory. 

1. "./run_server.sh install" will install all required packages in a virtual environment. You will see a venv folder appear in the server directory after running this program. To activate this virtual environment, use the command: "source venv/bin/activate".
2. "./run_server.sh start" will start the server and the local host url will be provided in the terminal which you can then paste into a broweser to view. The url will be: http://localhost:8080. You can use: http://localhost:8080/docs to test out the api functionality.
3. "./run_server.sh test" will run all the testcases for the program and output results in "test_output.txt."
4. "./run_server.sh clean" will remove the virtual environment
5. "./run_server.sh -help" will also provide information on how to run the server. 

You will also need to set up a .env file in the server directory for the program to run properly. GOOGLE_CLOUD_PROJECT, BIGQUERY_DATASET GOOGLE_APPLICATION_CREDENTIALS, and GITHUB_TOKEN are the four different environment variables currently in use.




