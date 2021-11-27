# coding: utf-8

"""
    ECE 461 - Fall 2021 - Project 2

    API for ECE 461/Fall 2021/Project 2: A Trustworthy Module Registry

    The version of the OpenAPI document: 2.0.0
    Contact: davisjam@purdue.edu
    Generated by: https://openapi-generator.tech
"""


from fastapi import FastAPI

from openapi_server.apis.default_api import router as DefaultApiRouter

app = FastAPI(
    title="ECE 461 - Fall 2021 - Project 2",
    description="API for ECE 461/Fall 2021/Project 2: A Trustworthy Module Registry",
    version="2.0.0",
)
app.include_router(DefaultApiRouter)
