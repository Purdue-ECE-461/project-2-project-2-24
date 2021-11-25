# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, validator  # noqa: F401


class PackageData(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    PackageData - a model defined in OpenAPI

        content: The content of this PackageData [Optional].
        url: The url of this PackageData [Optional].
        js_program: The js_program of this PackageData [Optional].
    """

    content: Optional[str] = None
    url: Optional[str] = None
    js_program: Optional[str] = None

PackageData.update_forward_refs()
