# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, validator  # noqa: F401
from pydantic.fields import Field


class PackageQuery(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    PackageQuery - a model defined in OpenAPI

        version: The version of this PackageQuery [Optional].
        name: The name of this PackageQuery.
    """

    version: Optional[str] = Field(None, alias='Version')
    name: str = Field(..., alias='Name')

PackageQuery.update_forward_refs()
