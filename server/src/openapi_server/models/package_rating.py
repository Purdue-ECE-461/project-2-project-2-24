# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, validator  # noqa: F401


class PackageRating(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    PackageRating - a model defined in OpenAPI

        bus_factor: The bus_factor of this PackageRating.
        correctness: The correctness of this PackageRating.
        ramp_up: The ramp_up of this PackageRating.
        responsive_maintainer: The responsive_maintainer of this PackageRating.
        license_score: The license_score of this PackageRating.
        good_pinning_practice: The good_pinning_practice of this PackageRating.
    """

    bus_factor: float
    correctness: float
    ramp_up: float
    responsive_maintainer: float
    license_score: float
    good_pinning_practice: float

PackageRating.update_forward_refs()
