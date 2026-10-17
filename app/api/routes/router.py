
from fastapi import APIRouter

from app.api.routes.auth import (
    router as auth_router,
)

from app.api.routes.users import (
    router as users_router,
)

from app.api.routes.profiles import (
    router as profiles_router,
)
from app.api.routes.introduction_mcqs import (
    router as introduction_mcqs_router,
)
from app.api.routes.career_personas import (
    router as career_personas_router,
)

from app.api.routes.career_persona_history import (
    router as career_persona_history_router,
)

from app.api.routes.audit_logs import (
    router as audit_logs_router,
)

from app.api.routes.mentors import (
    router as mentors_router,
)

from app.api.routes.mentor_applications import (
    router as mentor_applications_router,
)

from app.api.routes import dashboard

from app.api.routes.notifications import (
    router as notifications_router,
)


from app.api.routes.courses import (
    router as courses_router,
)

from app.api.routes.levels import (
    router as levels_router,
)

from app.api.routes.checkpoints import (
    router as checkpoints_router,
)

from app.api.routes.progress import (
    router as progress_router,
)

from app.api.routes.master_data import (
    router as master_data_router,
)

from app.api.routes.files import (
    router as files_router,
)

from app.api.routes.journey import (
    router as journey_router,
)

from app.api.routes.course_journey import (
    router as course_journey_router,
)

from app.api.routes.career_calendar import (
    router as career_calendar_router,
)

from app.api.routes.code_execution import (
    router as code_execution_router,
)
from app.api.routes.student_school import (
    router as student_school_router,
)


from app.api.routes.school_packages import (
    router as school_packages_router,
)
from app.api.routes.student_courses import (
    router as student_courses_router,
)
from app.api.routes.schools import(
    router as school_router,
)
from app.api.routes.student_import import (
    router as student_import_router,
)
from app.api.routes.skill_assessment import (
    router as skill_assessment_router,
)
from app.api.routes.school_admin import (
    router as school_admin_router,
)
# ============================================================
# MAIN API ROUTER
# ============================================================

api_router = APIRouter()


# ============================================================
# COURSE JOURNEY
# ============================================================

api_router.include_router(
    course_journey_router
)


# ============================================================
# PUBLIC JOBS
# ============================================================

# ============================================================
# CAREER CALENDAR
# ============================================================

api_router.include_router(
    career_calendar_router
)


# ============================================================
# NOTIFICATIONS
# ============================================================

api_router.include_router(
    notifications_router
)


# ============================================================
# CODE EXECUTION
# ============================================================

api_router.include_router(
    code_execution_router
)


# ============================================================
# JOURNEY
# ============================================================

api_router.include_router(
    journey_router
)


# ============================================================
# AUTH
# ============================================================

api_router.include_router(
    auth_router
)


# ============================================================
# MASTER DATA
# ============================================================

api_router.include_router(
    master_data_router
)


# ============================================================
# USERS
# ============================================================

api_router.include_router(
    users_router
)


# ============================================================
# AUDIT LOGS
# ============================================================

api_router.include_router(
    audit_logs_router
)


# ============================================================
# FILES
# ============================================================

api_router.include_router(
    files_router
)
#============================================================
#introduction of mcq
#===========================================================
api_router.include_router(
    introduction_mcqs_router
)


# ============================================================
# PROFILES
# ============================================================

api_router.include_router(
    profiles_router
)


# ============================================================
# CAREER PERSONAS
# ============================================================

api_router.include_router(
    career_personas_router
)


# ============================================================
# CAREER PERSONA HISTORY
# ============================================================

api_router.include_router(
    career_persona_history_router
)


# ============================================================
# REPORT EXPORTS
# ============================================================



# ============================================================
# MENTORS
# ============================================================

api_router.include_router(
    mentors_router
)


# ============================================================
# WORK EXPERIENCE
# ============================================================

# ============================================================
# MENTOR APPLICATIONS
# ============================================================

api_router.include_router(
    mentor_applications_router
)


# ============================================================
# BOOKINGS
# ============================================================

# ============================================================
# COMPANIES
# ============================================================

# ============================================================
# COMPANY APPLICATIONS
# ============================================================

# ============================================================
# DASHBOARD
# ============================================================

api_router.include_router(
    dashboard.router
)


# ============================================================
# JOBS
# ============================================================

# ============================================================
# JOB APPLICATIONS
# ============================================================

# ============================================================
# COURSES
# ============================================================

api_router.include_router(
    courses_router
)


# ============================================================
# ORGANIZATIONS
# ============================================================

# ============================================================
# ORGANIZATION APPLICATIONS
# ============================================================

# ============================================================
# ORGANIZATION MEMBERS
# ============================================================

# ============================================================
# INTERVIEWS
# ============================================================




# ============================================================
# ORGANIZATION ANALYTICS
# ============================================================

# ============================================================
# ORGANIZATION DASHBOARD
# ============================================================

# ============================================================
# LEVELS
# ============================================================

api_router.include_router(
    levels_router
)


# ============================================================
# CHECKPOINTS
# ============================================================

api_router.include_router(
    checkpoints_router
)


# ============================================================
# PROGRESS
# ============================================================

api_router.include_router(
    progress_router
)
api_router.include_router(
    student_school_router
)
api_router.include_router(
    school_router
                          )
api_router.include_router(
    school_packages_router
)
api_router.include_router(
    student_courses_router
)
api_router.include_router(
    student_import_router
)
api_router.include_router(
    skill_assessment_router
)
api_router.include_router(
    school_admin_router
)