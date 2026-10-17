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
    get_current_user,
)
from app.database.database import get_db
from app.models.user import User
from app.schemas.school_package import (
    SchoolPackageCreate,
    SchoolPackageUpdate,
    SchoolPackageResponse,
    SchoolPackageCourseResponse,
)
from app.services.school_package_service import (
    SchoolPackageService,
)


router = APIRouter(
    prefix="/school-packages",
    tags=["School Packages"],
)


# ============================================================
# RESPONSE BUILDER
# ============================================================

def build_response(
    result: dict,
) -> SchoolPackageResponse:

    package = result["package"]

    courses = result["courses"]

    return SchoolPackageResponse(
        id=package.id,
        school_id=package.school_id,
        school_name=result["school_name"],
        package_name=package.package_name,
        description=package.description,
        course_ids=[
            course.id
            for course in courses
        ],
        courses=[
            SchoolPackageCourseResponse.model_validate(
                course
            )
            for course in courses
        ],
        created_at=package.created_at,
        updated_at=package.updated_at,
    )


# ============================================================
# CREATE SCHOOL PACKAGE
# ============================================================

@router.post(
    "",
    response_model=SchoolPackageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_school_package(
    data: SchoolPackageCreate,
    current_user: User = Depends(
        get_current_user
    ),
    session: AsyncSession = Depends(
        get_db
    ),
):

    service = SchoolPackageService(
        session
    )

    result = await service.create_package(
        school_id=data.school_id,
        package_name=data.package_name,
        description=data.description,
        course_ids=data.course_ids,
    )

    return build_response(result)


# ============================================================
# GET ALL PACKAGES
# ============================================================

@router.get(
    "",
    response_model=list[SchoolPackageResponse],
)
async def get_school_packages(
    school_id: UUID | None = Query(
        default=None,
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
        get_current_user
    ),
    session: AsyncSession = Depends(
        get_db
    ),
):

    service = SchoolPackageService(
        session
    )

    results = await service.get_packages(
        school_id=school_id,
        skip=skip,
        limit=limit,
    )

    return [
        build_response(result)
        for result in results
    ]


# ============================================================
# GET PACKAGE BY ID
# ============================================================

@router.get(
    "/{package_id}",
    response_model=SchoolPackageResponse,
)
async def get_school_package(
    package_id: UUID,
    current_user: User = Depends(
        get_current_user
    ),
    session: AsyncSession = Depends(
        get_db
    ),
):

    service = SchoolPackageService(
        session
    )

    result = await service.get_package(
        package_id
    )

    return build_response(result)


# ============================================================
# UPDATE PACKAGE
# ============================================================

@router.put(
    "/{package_id}",
    response_model=SchoolPackageResponse,
)
async def update_school_package(
    package_id: UUID,
    data: SchoolPackageUpdate,
    current_user: User = Depends(
        get_current_user
    ),
    session: AsyncSession = Depends(
        get_db
    ),
):

    service = SchoolPackageService(
        session
    )

    result = await service.update_package(
        package_id,
        package_name=data.package_name,
        description=data.description,
        course_ids=data.course_ids,
    )

    return build_response(result)


# ============================================================
# DELETE PACKAGE
# ============================================================

@router.delete(
    "/{package_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_school_package(
    package_id: UUID,
    current_user: User = Depends(
        get_current_user
    ),
    session: AsyncSession = Depends(
        get_db
    ),
):

    service = SchoolPackageService(
        session
    )

    await service.delete_package(
        package_id
    )

    return None