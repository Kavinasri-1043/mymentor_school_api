from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job import Job
from app.repositories.base import BaseRepository


class JobRepository(BaseRepository[Job]):
    """
    Repository responsible for Job database operations.

    Business rules belong in the service layer.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(Job, session)

    # ============================================================
    # GET BY COMPANY ID
    # ============================================================

    async def get_by_company_id(
        self,
        company_id: UUID,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Job]:

        result = await self.session.execute(
            select(Job)
            .where(
                Job.company_id == company_id
            )
            .order_by(
                Job.created_at.desc()
            )
            .offset(skip)
            .limit(limit)
        )

        return list(
            result.scalars().all()
        )

    # ============================================================
    # GET BY POSTED USER
    # ============================================================

    async def get_by_posted_by(
        self,
        user_id: UUID,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Job]:

        result = await self.session.execute(
            select(Job)
            .where(
                Job.posted_by == user_id
            )
            .order_by(
                Job.created_at.desc()
            )
            .offset(skip)
            .limit(limit)
        )

        return list(
            result.scalars().all()
        )

    # ============================================================
    # GET BY STATUS
    # ============================================================

    async def get_by_status(
        self,
        status: str,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Job]:

        result = await self.session.execute(
            select(Job)
            .where(
                Job.status == status
            )
            .order_by(
                Job.created_at.desc()
            )
            .offset(skip)
            .limit(limit)
        )

        return list(
            result.scalars().all()
        )

    # ============================================================
    # GET OPEN / ACTIVE JOBS
    # ============================================================

    async def get_open_jobs(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Job]:

        result = await self.session.execute(
            select(Job)
            .where(
                Job.status == "active"
            )
            .order_by(
                Job.created_at.desc()
            )
            .offset(skip)
            .limit(limit)
        )

        return list(
            result.scalars().all()
        )

    # ============================================================
    # GET BY TITLE
    # ============================================================

    async def get_by_title(
        self,
        title: str,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Job]:

        result = await self.session.execute(
            select(Job)
            .where(
                Job.title == title
            )
            .order_by(
                Job.created_at.desc()
            )
            .offset(skip)
            .limit(limit)
        )

        return list(
            result.scalars().all()
        )

    # ============================================================
    # GET BY LOCATION
    # ============================================================

    async def get_by_location(
        self,
        location: str,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Job]:

        result = await self.session.execute(
            select(Job)
            .where(
                Job.location == location
            )
            .order_by(
                Job.created_at.desc()
            )
            .offset(skip)
            .limit(limit)
        )

        return list(
            result.scalars().all()
        )