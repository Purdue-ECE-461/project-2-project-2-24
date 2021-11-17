from __future__ import absolute_import
from openapi_server.database import database
from openapi_server.models.package import Package
from openapi_server.models.package_data import PackageData
from openapi_server.models.package_metadata import PackageMetadata
from openapi_server.models.user import User
from dotenv import load_dotenv

load_dotenv()

db = database.Database()

user = User(name="Aiden", is_admin=True)
new_user = User(name="Matthew", is_admin=False)
package =  Package(
    metadata= PackageMetadata(name="PackageName", version="1.2.3", id="5"), 
    data= PackageData(content="packagecontent", url="https://www.package.url", js_program="javascript_code;")
)

def test_upload_package():
    db.upload_package(token="example_token", package=package)

if __name__ == "__main__":
    test_upload_package()
