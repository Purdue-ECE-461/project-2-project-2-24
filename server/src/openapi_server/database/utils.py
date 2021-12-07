import base64
import hashlib
import os
import tempfile
import zipfile
from scorer.src import url_handler


def db_hash(content):
    return hashlib.sha256(content.encode()).hexdigest()


def get_url_from_content(content):
    # Get decoded file contents
    decoded_contents = base64.b64decode(content)

    # Write to temporary file
    tmpfile = tempfile.TemporaryFile()
    with open(tmpfile.name, "wb") as writefile:
        writefile.write(decoded_contents)

    zipped_repo = zipfile.ZipFile(tmpfile.name)
    for filename in zipped_repo.namelist():
        if not os.path.isdir(filename):
            for line in zipped_repo.open(filename):
                if "homepage" in str(line):
                    result = str(line, 'utf-8')
                    result = result.rstrip().split(',')[0].split(' ')[3].strip('\"')
                    clean_url = result.strip()
                    repo_url = url_handler.get_github_url(clean_url)
                    zipped_repo.close()
                    return repo_url
