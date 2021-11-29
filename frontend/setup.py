"""
    ECE 461 - Fall 2021 - Project 2 - Team 24

    Expanded API for ECE 461/Fall 2021/Project 2/Team 24: A Trustworthy Module Registry  # noqa: E501

    The version of the OpenAPI document: 2.0.0
    Contact: gonza487@purdue.edu
    Generated by: https://openapi-generator.tech
"""


from setuptools import setup, find_packages  # noqa: H301

NAME = "openapi-client"
VERSION = "1.0.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
  "urllib3 >= 1.25.3",
  "python-dateutil",
]

setup(
    name=NAME,
    version=VERSION,
    description="ECE 461 - Fall 2021 - Project 2 - Team 24",
    author="Aiden Gonzalez",
    author_email="gonza487@purdue.edu",
    url="",
    keywords=["OpenAPI", "OpenAPI-Generator", "ECE 461 - Fall 2021 - Project 2 - Team 24"],
    python_requires=">=3.6",
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    license="Apache 2.0",
    long_description="""\
    Expanded API for ECE 461/Fall 2021/Project 2/Team 24: A Trustworthy Module Registry  # noqa: E501
    """
)
