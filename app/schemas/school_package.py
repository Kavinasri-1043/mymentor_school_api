from datetime import datetime
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


# ============================================================
# CREATE PACKAGE
# ============================================================

class SchoolPackageCreate(BaseModel):

    school_id: UUID

    package_name: str = Field(
        ...,
        min_length=2,
        max_length=255,
    )

    description: str | None = None

    course_ids: list[UUID] = Field(
        ...,
        min_length=1,
    )


# ============================================================
# UPDATE PACKAGE
# ============================================================

class SchoolPackageUpdate(BaseModel):

    package_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=255,
    )

    description: str | None = None

    course_ids: list[UUID] | None = None


# ============================================================
# COURSE INSIDE PACKAGE
# ============================================================

class SchoolPackageCourseResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    title: str
    description: str | None
    language: str
    difficulty: str
    duration: str | None
    thumbnail: str | None
    status: str


# ============================================================
# PACKAGE RESPONSE
# ============================================================

class SchoolPackageResponse(BaseModel):

    id: UUID

    school_id: UUID

    school_name: str

    package_name: str

    description: str | None

    course_ids: list[UUID]

    courses: list[
        SchoolPackageCourseResponse
    ]

    created_at: datetime

    updated_at: datetime