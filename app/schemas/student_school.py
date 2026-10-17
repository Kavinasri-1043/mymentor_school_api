from uuid import UUID

from pydantic import BaseModel, Field


# ============================================================
# SCHOOL CODE REQUEST
# ============================================================




class StudentCodeRequest(BaseModel):
    student_code: str = Field(
        ...,
        min_length=5,
        max_length=50,
    )


# ============================================================
# SCHOOL RESPONSE
# ============================================================

class StudentSchoolResponse(BaseModel):

    id: UUID
    name: str
    code: str
    school_type: str | None = None
    city: str
    state: str
    country: str
    status: str