from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.school_admin_repository import (
    SchoolAdminRepository,
)
from app.repositories.school_repository import (
    SchoolRepository,
)
from app.schemas.school_admin import (
    SchoolAdminDashboardResponse,
    SchoolAdminStudentItem,
    SchoolAdminStudentsResponse,
    SchoolAdminCourseItem,
    SchoolAdminCoursesResponse,
    SchoolAdminStudentSummary,
    SchoolAdminCourseSummary,
)


class SchoolAdminService:

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.repository = (
            SchoolAdminRepository(session)
        )

        self.school_repository = (
            SchoolRepository(session)
        )

    # ========================================================
    # DASHBOARD
    # ========================================================

    async def get_dashboard(
        self,
        school_id: UUID,
    ):

        school = await (
            self.school_repository.get_by_id(
                school_id
            )
        )

        if school is None:
            raise ValueError(
                "School not found."
            )

        total_students = await (
            self.repository.get_total_students(
                school_id
            )
        )

        active_students = await (
            self.repository.get_active_students(
                school_id
            )
        )

        courses = await (
            self.repository.get_assigned_courses(
                school_id,
                limit=1000,
            )
        )

        completed_levels = await (
            self.repository.get_completed_levels(
                school_id
            )
        )

        learning_videos = await (
            self.repository.get_learning_videos(
                school_id
            )
        )

        coding_challenges = await (
            self.repository.get_coding_challenges(
                school_id
            )
        )

        active_this_week = await (
            self.repository.get_active_this_week(
                school_id
            )
        )

        # ----------------------------------------------------
        # COURSE PERFORMANCE
        # ----------------------------------------------------

        course_performance = []

        total_progress = 0.0
        progress_course_count = 0

        for row in courses:

            levels = row.level_count or 0
            students = (
                row.enrollment_count or 0
            )
            completed = (
                row.completed_count or 0
            )

            if (
                levels > 0
                and students > 0
            ):
                progress = (
                    completed
                    / (levels * students)
                ) * 100
            else:
                progress = 0.0

            total_progress += progress
            progress_course_count += 1

            course_performance.append(
                SchoolAdminCourseSummary(
                    course_id=row.Course.id,
                    title=row.Course.title,
                    students=students,
                    levels=levels,
                    progress_percentage=round(
                        progress,
                        2,
                    ),
                )
            )

        average_progress = (
            total_progress
            / progress_course_count
            if progress_course_count
            else 0.0
        )

        # ----------------------------------------------------
        # RECENT STUDENTS
        # ----------------------------------------------------

        recent_rows = await (
            self.repository
            .get_recently_active_students(
                school_id
            )
        )

        recently_active_students = [
            SchoolAdminStudentSummary(
                id=row.id,
                name=row.name,
                email=row.email,
                student_code=row.student_code,
                xp=row.xp or 0,
                streak=row.streak or 0,
                levels=row.levels or 0,
            )
            for row in recent_rows
        ]

        return SchoolAdminDashboardResponse(
            school_id=school.id,
            school_name=school.name,
            school_code=school.code,

            total_students=total_students,
            active_students=active_students,

            assigned_courses=len(courses),
            average_progress=round(
                average_progress,
                2,
            ),

            completed_levels=completed_levels,
            learning_videos=learning_videos,
            coding_challenges=coding_challenges,
            active_this_week=active_this_week,

            recently_active_students=(
                recently_active_students
            ),

            course_performance=(
                course_performance
            ),
        )

    # ========================================================
    # STUDENTS
    # ========================================================

    async def get_students(
        self,
        school_id: UUID,
        search: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ):

        rows = await (
            self.repository.get_students(
                school_id=school_id,
                search=search,
                skip=skip,
                limit=limit,
            )
        )

        total = await (
            self.repository.count_students(
                school_id=school_id,
                search=search,
            )
        )

        students = []

        for row in rows:

            total_levels = (
                row.total_levels or 0
            )

            completed_levels = (
                row.level_count or 0
            )

            if total_levels > 0:
                progress = (
                    completed_levels
                    / total_levels
                ) * 100
            else:
                progress = 0.0

            students.append(
                SchoolAdminStudentItem(
                    id=row.User.id,
                    name=row.User.name,
                    email=row.User.email,
                    phone=row.User.phone,
                    student_code=(
                        row.User.student_code
                    ),
                    department=(
                        row.User.department
                    ),
                    year=row.User.year,

                    xp=row.User.xp or 0,
                    streak=row.User.streak or 0,

                    courses=(
                        row.course_count or 0
                    ),

                    levels=completed_levels,

                    progress_percentage=round(
                        progress,
                        2,
                    ),
                )
            )

        return SchoolAdminStudentsResponse(
            total=total,
            students=students,
        )

    # ========================================================
    # COURSES
    # ========================================================

    async def get_courses(
        self,
        school_id: UUID,
        search: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ):

        rows = await (
            self.repository.get_assigned_courses(
                school_id=school_id,
                search=search,
                skip=skip,
                limit=limit,
            )
        )

        courses = []

        total_enrollments = 0
        total_levels = 0
        total_progress = 0.0

        for row in rows:

            levels = row.level_count or 0
            students = (
                row.enrollment_count or 0
            )
            completed = (
                row.completed_count or 0
            )

            if levels > 0 and students > 0:
                progress = (
                    completed
                    / (levels * students)
                ) * 100
            else:
                progress = 0.0

            total_enrollments += students
            total_levels += levels
            total_progress += progress

            courses.append(
                SchoolAdminCourseItem(
                    course_id=row.Course.id,
                    title=row.Course.title,
                    description=(
                        row.Course.description
                    ),
                    category=row.Course.category,
                    language=row.Course.language,
                    difficulty=row.Course.difficulty,
                    duration=row.Course.duration,
                    thumbnail=row.Course.thumbnail,

                    students=students,
                    levels=levels,

                    progress_percentage=round(
                        progress,
                        2,
                    ),
                )
            )

        average_progress = (
            total_progress / len(courses)
            if courses
            else 0.0
        )

        return SchoolAdminCoursesResponse(
            total_courses=len(courses),
            total_enrollments=(
                total_enrollments
            ),
            total_levels=total_levels,
            average_progress=round(
                average_progress,
                2,
            ),
            courses=courses,
        )