from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.school import School
from app.repositories.school_repository import (
    SchoolRepository,
)
from app.utils.school_code import (
    generate_school_code,
)

class SchoolService:

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.repository = SchoolRepository(
            session
        )

    # ========================================================
    # GET BY ID
    # ========================================================

    async def get_by_id(
        self,
        school_id: UUID,
    ) -> School | None:

        return await self.repository.get_by_id(
            school_id
        )

    # ========================================================
    # GET BY CODE
    # ========================================================

    async def get_by_code(
        self,
        code: str,
    ) -> School | None:

        return await self.repository.get_by_code(
            code
        )

    # ========================================================
    # GET BY NAME
    # ========================================================

    async def get_by_name(
        self,
        name: str,
    ) -> School | None:

        return await self.repository.get_by_name(
            name
        )

    # ========================================================
    # GET SCHOOLS
    # ========================================================

    async def get_schools(
        self,
        *,
        search: str | None = None,
        school_type: str | None = None,
        status: str | None = None,
        city: str | None = None,
        state: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[School]:

        return await self.repository.get_schools(
            search=search,
            school_type=school_type,
            status=status,
            city=city,
            state=state,
            skip=skip,
            limit=limit,
        )

    # ========================================================
    # CREATE
    # ========================================================

    async def create(
        self,
        school: School,
    ) -> School:

        return await self.repository.create(
            school
        )

    # ========================================================
    # UPDATE
    # ========================================================

    async def update(
        self,
        school: School,
    ) -> School:

        return await self.repository.update(
            school
        )

    # ========================================================
    # DELETE
    # ========================================================

    async def delete(
        self,
        school: School,
    ) -> None:

        await self.repository.delete(
            school
        )
    async def generate_unique_code(
        self,
        school_name: str,
    ) -> str:

        for _ in range(20):

            code = generate_school_code(
                school_name
            )

            existing = await self.repository.get_by_code(
                code
            )

            if existing is None:
                return code

        raise RuntimeError(
            "Unable to generate a unique school code."
        )