# School Backend

This is a school-oriented adaptation of the uploaded MyMentor backend. College terminology in application source and route/schema/model filenames has been changed to School, including the API prefixes and related role/field names.

The following screenshot-listed API groups have been removed from the active API router: public jobs, work experiences, bookings, companies, company applications, jobs, job applications, organizations, organization applications, organization members, organization analytics, and organization dashboard. Their source files are retained but are not mounted.

## Run
1. Create/activate your Python environment.
2. Install dependencies from `requirements.txt`.
3. Configure environment variables using `.env.example` (the original `.env` with secrets is intentionally not included).
4. Apply database migrations with `alembic upgrade head`.
5. Start the FastAPI app using the command documented in your project setup (typically `uvicorn app.main:app --reload`).

Review database migration history and environment configuration before running against an existing database; this adaptation changes college-related names to school-related names.
