from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "blacklistaccesstoken" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "access_token" VARCHAR(255) NOT NULL UNIQUE,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "blacklistrefreshtoken" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "refresh_token" VARCHAR(255) NOT NULL UNIQUE,
    "expires_at" TIMESTAMP NOT NULL,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "refreshtoken" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "refresh_token" VARCHAR(255) NOT NULL UNIQUE,
    "expires_at" TIMESTAMP NOT NULL,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
        ALTER TABLE "users" ADD CONSTRAINT "fk_users_companie_606fb13a" FOREIGN KEY ("company_id") REFERENCES "companies" ("id") ON DELETE SET NULL;
        ALTER TABLE "companies" ADD CONSTRAINT "fk_companie_users_184eb8c7" FOREIGN KEY ("director_id") REFERENCES "users" ("id") ON DELETE SET NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "companies" DROP FOREIGN KEY "fk_companie_users_184eb8c7";
        ALTER TABLE "users" DROP FOREIGN KEY "fk_users_companie_606fb13a";
        ALTER TABLE "users" DROP COLUMN "company_id";
        ALTER TABLE "companies" DROP COLUMN "director_id";
        DROP TABLE IF EXISTS "blacklistrefreshtoken";
        DROP TABLE IF EXISTS "refreshtoken";
        DROP TABLE IF EXISTS "blacklistaccesstoken";"""
