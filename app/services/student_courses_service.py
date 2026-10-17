from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.school_package import SchoolPackage
from app.models.school_package_course import SchoolPackageCourse
from app.models.school import School
from app.models.course import Course
from app.models.course_enrollment import CourseEnrollment
from app.models.user import User


class StudentCoursesService:

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def get_student_courses(
        self,
        user: User,
    ):

        # ====================================================
        # 1. GET INDIVIDUALLY ENROLLED COURSES
        # ====================================================

        enrollment_result = await self.session.execute(
            select(
                CourseEnrollment,
                Course,
            )
            .join(
                Course,
                Course.id == CourseEnrollment.course_id,
            )
            .where(
                CourseEnrollment.user_id == user.id
            )
        )

        enrolled_rows = enrollment_result.all()

        enrolled_courses = []

        enrolled_course_ids: set[UUID] = set()

        for enrollment, course in enrolled_rows:

            enrolled_course_ids.add(course.id)

            enrolled_courses.append(
                {
                    "course_id": course.id,
                    "course_name": course.title,
                    "description": getattr(
                        course,
                        "description",
                        None,
                    ),
                    "enrolled": True,
                    "package_course": False,
                    "package_id": None,
                    "package_name": None,
                }
            )

        # ====================================================
        # 2. GET SCHOOL PACKAGE COURSES
        # ====================================================

        package_courses = []

        if user.school_id:

            package_result = await self.session.execute(
                select(
                    SchoolPackage,
                    Course,
                )
                .join(
                    SchoolPackageCourse,
                    SchoolPackageCourse.package_id
                    == SchoolPackage.id,
                )
                .join(
                    Course,
                    Course.id
                    == SchoolPackageCourse.course_id,
                )
                .where(
                    SchoolPackage.school_id
                    == user.school_id
                )
            )

            package_rows = package_result.all()

            package_course_ids: set[UUID] = set()

            for package, course in package_rows:

                # Prevent duplicate courses if the same course
                # exists in multiple packages.
                if course.id in package_course_ids:
                    continue

                package_course_ids.add(course.id)

                package_courses.append(
                    {
                        "course_id": course.id,
                        "course_name": course.title,
                        "description": getattr(
                            course,
                            "description",
                            None,
                        ),
                        "enrolled": (
                            course.id
                            in enrolled_course_ids
                        ),
                        "package_course": True,
                        "package_id": package.id,
                        "package_name": package.package_name,
                    }
                )

        # ====================================================
        # 3. GET SCHOOL INFORMATION
        # ====================================================

        school_name = None
        school_code = None

        if user.school_id:
            school_result = await self.session.execute(
                select(School).where(
                    School.id == user.school_id
                )
            )

            school = school_result.scalar_one_or_none()

            if school:
                school_name = school.name
                school_code = school.code

        # ====================================================
        # 4. COMBINE COURSES
        # ====================================================

        combined_courses = []
        added_course_ids: set[UUID] = set()

        # Package courses first
        for course in package_courses:
            if course["course_id"] in added_course_ids:
                continue

            added_course_ids.add(course["course_id"])
            combined_courses.append(course)

        # Then individually enrolled courses
        for course in enrolled_courses:
            if course["course_id"] in added_course_ids:
                continue

            added_course_ids.add(course["course_id"])
            combined_courses.append(course)

        # ====================================================
        # 5. RETURN
        # ====================================================

        return {
            "school_id": user.school_id,
            "school_name": school_name,
            "school_code": school_code,
            "package_courses": package_courses,
            "enrolled_courses": enrolled_courses,
            "courses": combined_courses,
        }