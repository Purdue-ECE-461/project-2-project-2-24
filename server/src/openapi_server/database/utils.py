import base64
import binascii
import hashlib
import os
import tempfile
import zipfile
from openapi_server.scorer.src import url_handler

INVALID_CONTENTS_MESSAGE = "INVALID CONTENT ENCODING!"
NO_URL_MESSAGE = "NO PACKAGE URL DETECTED"


def db_hash(content):
    return hashlib.sha256(content.encode()).hexdigest()


def db_b64_encode(content):
    return base64.b64encode(content).decode("utf-8")


def get_url_from_content(content):
    # Get decoded file contents
    try:
        decoded_contents = base64.b64decode(content)
    except binascii.Error:
        return INVALID_CONTENTS_MESSAGE

    # Write to temporary file
    tmpfile = tempfile.NamedTemporaryFile()
    with open(tmpfile.name, "wb") as writefile:
        writefile.write(decoded_contents)

    try:
        zipped_repo = zipfile.ZipFile(tmpfile.name)
    except zipfile.BadZipFile:
        return INVALID_CONTENTS_MESSAGE

    # Get URL from package.json
    for filename in zipped_repo.namelist():
        if os.path.basename(filename) == "package.json":
            for line in zipped_repo.open(filename):
                if "github" in str(line) or "npmjs" in str(line):
                    line_string = str(line, 'utf-8').strip()
                    segments = line_string.split('"')
                    clean_url = [i for i in segments if "github" in i or "npmjs" in i][0].strip()
                    if clean_url.endswith(".git"):
                        clean_url = clean_url[:-4]
                    repo_url = url_handler.get_github_url(clean_url)
                    zipped_repo.close()
                    return repo_url

    return NO_URL_MESSAGE
