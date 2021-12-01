import hashlib


def db_hash(content):
    return hashlib.sha256(content.encode()).hexdigest()
