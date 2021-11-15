from __future__ import absolute_import
from database import database
from models import *
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
    db.upload_package(user=user, package=package)

def test_create_new_user():
    db.create_new_user(user=user, new_user=user)
