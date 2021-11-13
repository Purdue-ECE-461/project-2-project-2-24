from __future__ import absolute_import
from openapi_server.database import database
from openapi_server.models import *
from dotenv import load_dotenv


load_dotenv()
db = database.Database()

user = User(name="Aiden", is_admin=False)
package =  Package(
    metadata= PackageMetadata(name="PackageName", version="1.2.3", id="5"), 
    data= PackageData(content="packagecontent", url="https://www.package.url", js_program="javascript_code;")
)

def test_upload_package():
    db.upload_package(user=user, package=package)
