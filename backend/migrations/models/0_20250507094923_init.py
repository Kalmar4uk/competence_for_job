from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "password" VARCHAR(128) NOT NULL,
    "first_name" VARCHAR(50) NOT NULL,
    "last_name" VARCHAR(100) NOT NULL,
    "middle_name" VARCHAR(100),
    "job_title" VARCHAR(50),
    "date_of_employment" DATE,
    "is_active" INT NOT NULL DEFAULT 1,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "companies" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(250) NOT NULL UNIQUE,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "closed_at" TIMESTAMP,
    "is_active" INT NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS "legaldetailscompany" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "company_id" INT NOT NULL REFERENCES "companies" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "oldcompanyemployee" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "job_title" VARCHAR(50) NOT NULL,
    "date_of_emplyment" DATE,
    "date_of_dismissal" DATE,
    "company_id" INT REFERENCES "companies" ("id") ON DELETE SET NULL,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "gradeskill" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "grade" VARCHAR(10) NOT NULL,
    "evaluation_number" SMALLINT NOT NULL
);
CREATE TABLE IF NOT EXISTS "skill" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "area_of_application" VARCHAR(11) NOT NULL,
    "skill" VARCHAR(150) NOT NULL
);
CREATE TABLE IF NOT EXISTS "templatematrix" (
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(100) NOT NULL,
    "author_id" INT REFERENCES "users" ("id") ON DELETE SET NULL,
    "company_id" INT REFERENCES "companies" ("id") ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS "matrix" (
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(20) NOT NULL DEFAULT 'Назначенная матрица',
    "status" VARCHAR(10) NOT NULL,
    "last_update_status" TIMESTAMP,
    "completed_at" TIMESTAMP,
    "deadline" TIMESTAMP,
    "template_matrix_id" INT NOT NULL REFERENCES "templatematrix" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "gradeskillmatrix" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "grades_id" INT NOT NULL DEFAULT 1 REFERENCES "gradeskill" ("id") ON DELETE CASCADE,
    "matrix_id" INT NOT NULL REFERENCES "matrix" ("id") ON DELETE CASCADE,
    "skills_id" INT NOT NULL REFERENCES "skill" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);
CREATE TABLE IF NOT EXISTS "templatematrix_skill" (
    "templatematrix_id" INT NOT NULL REFERENCES "templatematrix" ("id") ON DELETE CASCADE,
    "skill_id" INT NOT NULL REFERENCES "skill" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_templatemat_templat_097d5e" ON "templatematrix_skill" ("templatematrix_id", "skill_id");
CREATE TABLE IF NOT EXISTS "matrix.GradeSkillMatrix" (
    "matrix_id" INT NOT NULL REFERENCES "matrix" ("id") ON DELETE CASCADE,
    "skill_id" INT NOT NULL REFERENCES "skill" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_matrix.Grad_matrix__4f6e79" ON "matrix.GradeSkillMatrix" ("matrix_id", "skill_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
