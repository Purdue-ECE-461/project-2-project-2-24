# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "openapi_server"
VERSION = "1.0.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "python-dotenv",
    "connexion[swagger-ui] >= 2.6.0",
    "werkzeug == 0.16.1",
    "swagger-ui-bundle >= 0.0.2",
    "python_dateutil >= 2.6.0",
    "setuptools >= 21.0.0",
    "Flask == 1.1.2",
    "google-cloud-bigquery",
    "pytest~=4.6.7", # needed for python 2.7+3.4
    "pytest-cov>=2.8.1",
    "pytest-randomly==1.2.3", # needed for python 2.7+3.4
    "Flask-Testing==0.8.0",
    "coverage"
]

setup(
    name=NAME,
    version=VERSION,
    description="ECE 461 - Fall 2021 - Project 2",
    author_email="davisjam@purdue.edu",
    url="",
    keywords=["OpenAPI", "ECE 461 - Fall 2021 - Project 2"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['openapi/openapi.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['openapi_server=openapi_server.__main__:main']},
    long_description="""\
    API for ECE 461/Fall 2021/Project 2: A Trustworthy Module Registry
    """
)

