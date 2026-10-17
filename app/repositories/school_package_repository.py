from typing import Optional
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.school_package import SchoolPackage
from app.models.school_package_course import (
    SchoolPackageCourse,
)
from app.models.school import School
from app.models.course import Course
from app.repositories.base import BaseRepository


class SchoolPackageRepository(
    BaseRepository[SchoolPackage]
):

    def __init__(
        self,
        session: AsyncSession,
    ):
        super().__init__(
            SchoolPackage,
            session,
        )

    # ========================================================
    # GET PACKAGE WITH COURSES
    # ========================================================

    async def get_by_id_with_courses(
        self,
        package_id: UUID,
    ) -> Optional[dict]:

        package_result = await self.session.execute(
            select(
                SchoolPackage,
                School.name.label(
                    "school_name"
                ),
            )
            .join(
                School,
                School.id
                == SchoolPackage.school_id,
            )
            .where(
                SchoolPackage.id == package_id
            )
        )

        row = package_result.first()

        if row is None:
            return None

        package = row[0]
        school_name = row[1]

        course_result = await self.session.execute(
            select(Course)
            .join(
                SchoolPackageCourse,
                SchoolPackageCourse.course_id
                == Course.id,
            )
            .where(
                SchoolPackageCourse.package_id
                == package_id
            )
            .order_by(
                Course.created_at.asc()
            )
        )

        courses = list(
            course_result.scalars().all()
        )

        return {
            "package": package,
            "school_name": school_name,
            "courses": courses,
        }

    # ========================================================
    # GET ALL PACKAGES
    # ========================================================

    async def get_all_with_courses(
        self,
        *,
        school_id: UUID | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[dict]:

        query = (
            select(
                SchoolPackage,
                School.name.label(
                    "school_name"
                ),
            )
            .join(
                School,
                School.id
                == SchoolPackage.school_id,
            )
        )

        if school_id is not None:
            query = query.where(
                SchoolPackage.school_id
                == school_id
            )

        query = (
            query
            .order_by(
                SchoolPackage.created_at.desc()
            )
            .offset(skip)
            .limit(limit)
        )

        result = await self.session.execute(
            query
        )

        rows = result.all()

        response = []

        for row in rows:

            package = row[0]
            school_name = row[1]

            course_result = (
                await self.session.execute(
                    select(Course)
                    .join(
                        SchoolPackageCourse,
                        SchoolPackageCourse.course_id
                        == Course.id,
                    )
                    .where(
                        SchoolPackageCourse.package_id
                        == package.id
                    )
                    .order_by(
                        Course.created_at.asc()
                    )
                )
            )

            courses = list(
                course_result.scalars().all()
            )

            response.append(
                {
                    "package": package,
                    "school_name": school_name,
                    "courses": courses,
                }
            )

        return response

    # ========================================================
    # FIND PACKAGE BY SCHOOL + NAME
    # ========================================================

    async def get_by_school_and_name(
        self,
        school_id: UUID,
        package_name: str,
    ) -> Optional[SchoolPackage]:

        result = await self.session.execute(
            select(SchoolPackage).where(
                SchoolPackage.school_id
                == school_id,
                SchoolPackage.package_name
                == package_name,
            )
        )

        return result.scalar_one_or_none()

    # ========================================================
    # ADD COURSES
    # ========================================================

    async def add_courses(
        self,
        package_id: UUID,
        course_ids: list[UUID],
    ) -> None:

        for course_id in course_ids:

            self.session.add(
                SchoolPackageCourse(
                    package_id=package_id,
                    course_id=course_id,
                )
            )

    # ========================================================
    # REMOVE ALL COURSES
    # ========================================================

    async def remove_courses(
        self,
        package_id: UUID,
    ) -> None:

        await self.session.execute(
            delete(
                SchoolPackageCourse
            ).where(
                SchoolPackageCourse.package_id
                == package_id
            )
        )