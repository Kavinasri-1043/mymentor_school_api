from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.school import School
from app.repositories.base import BaseRepository


class SchoolRepository(
    BaseRepository[School]
):

    def __init__(
        self,
        session: AsyncSession,
    ):
        super().__init__(
            School,
            session,
        )

    # ========================================================
    # GET BY CODE
    # ========================================================

    async def get_by_code(
        self,
        code: str,
    ) -> School | None:

        result = await self.session.execute(
            select(School).where(
                School.code == code
            )
        )

        return result.scalar_one_or_none()

    # ========================================================
    # GET BY NAME
    # ========================================================

    async def get_by_name(
        self,
        name: str,
    ) -> School | None:

        result = await self.session.execute(
            select(School).where(
                School.name.ilike(name)
            )
        )

        return result.scalar_one_or_none()

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

        query = select(School)

        # ----------------------------------------------------
        # SEARCH
        # ----------------------------------------------------

        if search:

            search_value = (
                f"%{search.strip()}%"
            )

            query = query.where(
                or_(
                    School.name.ilike(
                        search_value
                    ),
                    School.code.ilike(
                        search_value
                    ),
                    School.city.ilike(
                        search_value
                    ),
                    School.state.ilike(
                        search_value
                    ),
                )
            )

        # ----------------------------------------------------
        # SCHOOL TYPE
        # ----------------------------------------------------

        if school_type:

            query = query.where(
                School.school_type
                == school_type
            )

        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        if status:

            query = query.where(
                School.status == status
            )

        # ----------------------------------------------------
        # CITY
        # ----------------------------------------------------

        if city:

            query = query.where(
                School.city.ilike(
                    f"%{city.strip()}%"
                )
            )

        # ----------------------------------------------------
        # STATE
        # ----------------------------------------------------

        if state:

            query = query.where(
                School.state.ilike(
                    f"%{state.strip()}%"
                )
            )

        query = (
            query
            .order_by(
                School.created_at.desc()
            )
            .offset(skip)
            .limit(limit)
        )

        result = await self.session.execute(
            query
        )

        return list(
            result.scalars().all()
        )