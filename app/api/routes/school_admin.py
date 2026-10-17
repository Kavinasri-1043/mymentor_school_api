from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import (
    get_current_school_admin,
)
from app.database.database import get_db
from app.models.user import User
from app.schemas.school_admin import (
    SchoolAdminDashboardResponse,
    SchoolAdminStudentsResponse,
    SchoolAdminCoursesResponse,
)
from app.services.school_admin_service import (
    SchoolAdminService,
)
from app.services.auth_service import AuthService
from app.schemas.auth import LoginRequest
from app.models.school import School
from app.repositories.school_repository import SchoolRepository


router = APIRouter(
    prefix="/school-admin",
    tags=["School Admin"],
)
@router.post(
    "/login",
)
async def school_admin_login(
    data: LoginRequest,
    session: AsyncSession = Depends(get_db),
):
    service = AuthService(session)

    # --------------------------------------------------------
    # AUTHENTICATE EMAIL + PASSWORD
    # --------------------------------------------------------

    user = await service.authenticate(
        email=data.email,
        password=data.password,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    # --------------------------------------------------------
    # CHECK ROLE
    # --------------------------------------------------------

    if user.role != "school_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="School admin access required.",
        )

    # --------------------------------------------------------
    # CHECK SCHOOL LINK
    # --------------------------------------------------------

    if user.school_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="School admin is not linked to a school.",
        )

    # --------------------------------------------------------
    # GET SCHOOL
    # --------------------------------------------------------

    school_repository = SchoolRepository(
        session
    )

    school = await school_repository.get_by_id(
        user.school_id
    )

    if school is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="School not found.",
        )

    # --------------------------------------------------------
    # CREATE JWT
    # --------------------------------------------------------

    access_token = service.create_token(
        user
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "role": user.role,
        "school_id": school.id,
        "school_name": school.name,
        "school_code": school.code,
    }
@router.get(
    "/dashboard",
    response_model=SchoolAdminDashboardResponse,
)
async def get_school_admin_dashboard(
    current_user: User = Depends(
        get_current_school_admin
    ),
    session: AsyncSession = Depends(
        get_db
    ),
):

    service = SchoolAdminService(
        session
    )

    try:

        return await service.get_dashboard(
            current_user.school_id
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )


# ============================================================
# STUDENTS
# ============================================================

@router.get(
    "/students",
    response_model=SchoolAdminStudentsResponse,
)
async def get_school_admin_students(
    search: str | None = Query(
        default=None
    ),
    skip: int = Query(
        default=0,
        ge=0,
    ),
    limit: int = Query(
        default=100,
        ge=1,
        le=100,
    ),
    current_user: User = Depends(
        get_current_school_admin
    ),
    session: AsyncSession = Depends(
        get_db
    ),
):

    service = SchoolAdminService(
        session
    )

    return await service.get_students(
        school_id=current_user.school_id,
        search=search,
        skip=skip,
        limit=limit,
    )


# ============================================================
# COURSES
# ============================================================

@router.get(
    "/courses",
    response_model=SchoolAdminCoursesResponse,
)
async def get_school_admin_courses(
    search: str | None = Query(
        default=None
    ),
    skip: int = Query(
        default=0,
        ge=0,
    ),
    limit: int = Query(
        default=100,
        ge=1,
        le=100,
    ),
    current_user: User = Depends(
        get_current_school_admin
    ),
    session: AsyncSession = Depends(
        get_db
    ),
):

    service = SchoolAdminService(
        session
    )

    return await service.get_courses(
        school_id=current_user.school_id,
        search=search,
        skip=skip,
        limit=limit,
    )