from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import (
    get_current_user,
)
from app.database.database import get_db
from app.models.user import User
from app.schemas.student_school import (
    StudentCodeRequest,
    StudentSchoolResponse,
)
from app.services.student_school_service import (
    StudentSchoolService,
)


router = APIRouter(
    prefix="/students",
    tags=["Student School"],
)


# ============================================================
# LINK STUDENT TO SCHOOL
# ============================================================
@router.post(
    "/student-code",
    response_model=StudentSchoolResponse,
)
async def link_school_by_student_code(
    data: StudentCodeRequest,
    current_user: User = Depends(
        get_current_user
    ),
    session: AsyncSession = Depends(
        get_db
    ),
):

    service = StudentSchoolService(session)

    school = await service.link_school_by_student_code(
        current_user=current_user,
        student_code=data.student_code,
    )

    return StudentSchoolResponse(
        id=school.id,
        name=school.name,
        code=school.code,
        school_type=school.school_type,
        city=school.city,
        state=school.state,
        country=school.country,
        status=school.status,
    )