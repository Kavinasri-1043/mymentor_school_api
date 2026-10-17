from fastapi import HTTPException, status
from sqlalchemy import select

from app.models.school import School
from app.models.user import User


class StudentSchoolService:

    def __init__(self, session):
        self.session = session

    async def link_school_by_student_code(
        self,
        current_user: User,
        student_code: str,
    ) -> School:

        code = student_code.strip().upper()

        if not code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student ID is required.",
            )

        # --------------------------------------------------
        # FIND STUDENT BY STUDENT CODE
        # --------------------------------------------------

        result = await self.session.execute(
            select(User).where(
                User.student_code == code
            )
        )

        student = result.scalar_one_or_none()

        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid student ID.",
            )

        # --------------------------------------------------
        # MAKE SURE THE CODE BELONGS TO LOGGED-IN USER
        # --------------------------------------------------

        if student.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This student ID does not belong to the logged-in user.",
            )

        # --------------------------------------------------
        # STUDENT MUST HAVE A SCHOOL
        # --------------------------------------------------

        if student.school_id is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No school is assigned to this student.",
            )

        # --------------------------------------------------
        # FIND SCHOOL
        # --------------------------------------------------

        school_result = await self.session.execute(
            select(School).where(
                School.id == student.school_id
            )
        )

        school = school_result.scalar_one_or_none()

        if school is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="School not found.",
            )

        # --------------------------------------------------
        # CHECK SCHOOL STATUS
        # --------------------------------------------------

        if school.status.lower() != "active":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This school is currently inactive.",
            )

        # --------------------------------------------------
        # SAVE SCHOOL TO LOGGED-IN USER
        # --------------------------------------------------

        current_user.school_id = school.id

        await self.session.commit()
        await self.session.refresh(current_user)

        return school