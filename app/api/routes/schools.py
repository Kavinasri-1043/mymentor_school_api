from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import (
    get_current_system_admin,
)
from app.database.database import get_db
from app.models.school import School
from app.models.user import User
from app.schemas.school import (
    SchoolCreate,
    SchoolResponse,
    SchoolUpdate,
)
from app.services.school_service import (
    SchoolService,
)
from app.core.security import hash_password
from app.repositories.user_repository import UserRepository
from app.utils.password_encryption import encrypt_password
from app.utils.password_encryption import decrypt_password
router = APIRouter(
    prefix="/schools",
    tags=["Schools"],
)


# ============================================================
# CREATE SCHOOL
# ============================================================

@router.post(
    "",
    response_model=SchoolResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_school(
    data: SchoolCreate,
    current_user: User = Depends(
        get_current_system_admin
    ),
    session: AsyncSession = Depends(
        get_db
    ),
):
    """
    Create a new school.

    Admin only.
    """

    service = SchoolService(
        session
    )

    # --------------------------------------------------------
    # GENERATE UNIQUE SCHOOL CODE
    # --------------------------------------------------------

    code = await service.generate_unique_code(
        data.name.strip()
    )

    # --------------------------------------------------------
    # CREATE
    # --------------------------------------------------------

    school = School(
        name=data.name.strip(),
        code=code,
        school_type=data.school_type,
        established_year=data.established_year,
        university_affiliation=(
            data.university_affiliation
        ),
        accreditation=data.accreditation,
        email=data.email,
        phone=data.phone.strip(),
        website=data.website,
        principal_dean_name=(
            data.principal_dean_name
        ),
        contact_person=data.contact_person,
        address=data.address.strip(),
        city=data.city.strip(),
        state=data.state.strip(),
        country=data.country.strip(),
        pincode=data.pincode.strip(),
        description=data.description,
        status=data.status,
    )

    try:
        # --------------------------------------------------------
        # CREATE SCHOOL
        # --------------------------------------------------------

        created_school = await service.create(
            school
        )

        # --------------------------------------------------------
        # CHECK ADMIN EMAIL
        # --------------------------------------------------------

        user_repository = UserRepository(
            session
        )

        existing_admin = await user_repository.get_by_email(
            data.admin_email
        )

        if existing_admin is not None:
            await session.rollback()

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this admin email already exists.",
            )

        # --------------------------------------------------------
        # CREATE SCHOOL ADMIN USER
        # --------------------------------------------------------

        school_admin = User(
          name=f"{created_school.name} Admin",
          email=data.admin_email,
          password_hash=hash_password(data.admin_password),

        # Store encrypted copy for admin management
          admin_password_encrypted=encrypt_password(
             data.admin_password
         ),

          role="school_admin",
          school_id=created_school.id,
          is_active=True,
          is_verified=True,
         )

        await user_repository.create(
            school_admin
        )

        # --------------------------------------------------------
        # COMMIT BOTH SCHOOL + ADMIN
        # --------------------------------------------------------

        await session.commit()

    except IntegrityError:
        await session.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="School or admin email already exists.",
        )

    return SchoolResponse.model_validate(
        created_school
    )


# ============================================================
# GET ALL SCHOOLS
# ============================================================

@router.get(
    "",
    response_model=list[SchoolResponse],
)
async def get_schools(
    search: str | None = Query(
        default=None,
    ),
    school_type: str | None = Query(
        default=None,
    ),
    school_status: str | None = Query(
        default=None,
        alias="status",
    ),
    city: str | None = Query(
        default=None,
    ),
    state: str | None = Query(
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
        get_current_system_admin
    ),
    session: AsyncSession = Depends(
        get_db
    ),
):
    """
    Get schools with optional filters.

    Admin only.
    """

    service = SchoolService(
        session
    )

    schools = await service.get_schools(
    search=search,
    school_type=school_type,
    status=school_status,
    city=city,
    state=state,
    skip=skip,
    limit=limit,
)

    # --------------------------------------------------------
    # GET SCHOOL ADMIN EMAILS
    # --------------------------------------------------------

    # --------------------------------------------------------
    # GET SCHOOL ADMIN EMAIL + PASSWORD
    # --------------------------------------------------------

    school_ids = [
        school.id
        for school in schools
    ]

    admin_result = await session.execute(
        select(
            User.school_id,
            User.email,
            User.admin_password_encrypted,
        )
        .where(
            User.school_id.in_(school_ids),
            User.role == "school_admin",
        )
    )

    admin_map = {
        row.school_id: {
            "email": row.email,
            "password": (
                decrypt_password(row.admin_password_encrypted)
                if row.admin_password_encrypted
                else None
            ),
        }
        for row in admin_result.all()
    }

    # --------------------------------------------------------
    # BUILD RESPONSE
    # --------------------------------------------------------

    responses = []

    for school in schools:

        response = SchoolResponse.model_validate(
            school
        )

        admin = admin_map.get(school.id)

        if admin:
            response.admin_email = admin["email"]
            response.admin_password = admin["password"]

        responses.append(response)

    return responses


# ============================================================
# GET SCHOOL BY ID
# ============================================================

@router.get(
    "/{school_id}",
    response_model=SchoolResponse,
)
async def get_school(
    school_id: UUID,
    current_user: User = Depends(
        get_current_system_admin
    ),
    session: AsyncSession = Depends(
        get_db
    ),
):
    """
    Get a school by UUID.
    """

    service = SchoolService(
        session
    )

    school = await service.get_by_id(
        school_id
    )

    if school is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="School not found.",
        )

    # --------------------------------------------------------
    # GET SCHOOL ADMIN
    # --------------------------------------------------------

    admin_result = await session.execute(
        select(
            User.email,
            User.password_hash,
            User.admin_password_encrypted,
        )
        .where(
            User.school_id == school.id,
            User.role == "school_admin",
        )
    )

    admin = admin_result.first()

    # --------------------------------------------------------
    # BUILD RESPONSE
    # --------------------------------------------------------

    response = SchoolResponse.model_validate(
        school
    )

    if admin:
        response.admin_email = admin.email
        response.admin_password = (
            decrypt_password(admin.admin_password_encrypted)
            if admin.admin_password_encrypted
            else None
        )

    return response


# ============================================================
# UPDATE SCHOOL
# ============================================================

@router.put(
    "/{school_id}",
    response_model=SchoolResponse,
)
async def update_school(
    school_id: UUID,
    data: SchoolUpdate,
    current_user: User = Depends(
        get_current_system_admin
    ),
    session: AsyncSession = Depends(
        get_db
    ),
):
    """
    Update an existing school.

    Admin only.
    """

    service = SchoolService(
        session
    )

    school = await service.get_by_id(
        school_id
    )

    if school is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="School not found.",
        )

    

    # --------------------------------------------------------
    # UPDATE BASIC
    # --------------------------------------------------------

    if data.name is not None:
        school.name = data.name.strip()

    if data.school_type is not None:
        school.school_type = (
            data.school_type
        )

    if data.established_year is not None:
        school.established_year = (
            data.established_year
        )

    if data.university_affiliation is not None:
        school.university_affiliation = (
            data.university_affiliation
        )

    if data.accreditation is not None:
        school.accreditation = (
            data.accreditation
        )

    # --------------------------------------------------------
    # CONTACT
    # --------------------------------------------------------

    if data.email is not None:
        school.email = data.email

    if data.phone is not None:
        school.phone = data.phone.strip()

    if data.website is not None:
        school.website = data.website

    if data.principal_dean_name is not None:
        school.principal_dean_name = (
            data.principal_dean_name
        )

    if data.contact_person is not None:
        school.contact_person = (
            data.contact_person
        )

    # --------------------------------------------------------
    # ADDRESS
    # --------------------------------------------------------

    if data.address is not None:
        school.address = data.address.strip()

    if data.city is not None:
        school.city = data.city.strip()

    if data.state is not None:
        school.state = data.state.strip()

    if data.country is not None:
        school.country = data.country.strip()

    if data.pincode is not None:
        school.pincode = data.pincode.strip()

    # --------------------------------------------------------
    # ADDITIONAL
    # --------------------------------------------------------

    if data.description is not None:
        school.description = data.description

    if data.status is not None:
        school.status = data.status

    try:

        updated_school = (
            await service.update(
                school
            )
        )

        await session.commit()

    except IntegrityError:

        await session.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="School update failed.",
        )

    return SchoolResponse.model_validate(
        updated_school
    )


# ============================================================
# DELETE SCHOOL
# ============================================================

@router.delete(
    "/{school_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_school(
    school_id: UUID,
    current_user: User = Depends(
        get_current_system_admin
    ),
    session: AsyncSession = Depends(
        get_db
    ),
):
    """
    Delete a school.

    Admin only.
    """

    service = SchoolService(
        session
    )

    school = await service.get_by_id(
        school_id
    )

    if school is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="School not found.",
        )

    await service.delete(
        school
    )

    await session.commit()

    return None