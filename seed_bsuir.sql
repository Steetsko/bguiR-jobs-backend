
-- =========================================================
-- BSUIR Jobs — schema + minimal seed for local Postgres
-- DB: bsuir   USER: postgres   PASS: 111
-- Safe to re-run in dev (drops and recreates)
-- =========================================================
BEGIN;

-- ---------- Extensions ----------
CREATE EXTENSION IF NOT EXISTS citext;
CREATE EXTENSION IF NOT EXISTS pgcrypto;  -- for gen_random_uuid() if needed

-- ---------- Enums ----------
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_role') THEN
    CREATE TYPE user_role AS ENUM ('student','company','admin');
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'course_difficulty') THEN
    CREATE TYPE course_difficulty AS ENUM ('beginner','intermediate','advanced');
  END IF;
END $$;

-- ---------- Drop old tables (dev) ----------
DROP TABLE IF EXISTS coverage_results CASCADE;
DROP TABLE IF EXISTS student_skills CASCADE;
DROP TABLE IF EXISTS vacancy_skills CASCADE;
DROP TABLE IF EXISTS vacancies CASCADE;
DROP TABLE IF EXISTS course_skills CASCADE;
DROP TABLE IF EXISTS courses CASCADE;
DROP TABLE IF EXISTS skills CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- ---------- Tables ----------

-- users (UUID PK, CITEXT email, ENUM role)
CREATE TABLE users (
  user_id     UUID PRIMARY KEY,
  full_name   TEXT NOT NULL DEFAULT '',
  email       CITEXT NOT NULL UNIQUE,
  role        user_role NOT NULL DEFAULT 'student',
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- skills
CREATE TABLE skills (
  skill_id    SERIAL PRIMARY KEY,
  name        CITEXT NOT NULL UNIQUE,
  category    TEXT NOT NULL DEFAULT '',
  description TEXT NOT NULL DEFAULT ''
);

-- courses
CREATE TABLE courses (
  course_id       SERIAL PRIMARY KEY,
  title           TEXT NOT NULL,
  description     TEXT NOT NULL DEFAULT '',
  provider        TEXT NOT NULL DEFAULT '',
  duration_hours  INTEGER NOT NULL DEFAULT 0,
  difficulty      course_difficulty NOT NULL DEFAULT 'beginner'
);

-- course_skills (course ↔ skill) 0..1 weight, unique pair
CREATE TABLE course_skills (
  id               SERIAL PRIMARY KEY,
  course_id        INTEGER NOT NULL REFERENCES courses(course_id) ON DELETE CASCADE,
  skill_id         INTEGER NOT NULL REFERENCES skills(skill_id) ON DELETE CASCADE,
  coverage_weight  NUMERIC(3,2) NOT NULL DEFAULT 1.00,
  CONSTRAINT ck_course_skills_weight CHECK (coverage_weight >= 0.00 AND coverage_weight <= 1.00),
  CONSTRAINT uq_course_skill UNIQUE (course_id, skill_id)
);

-- vacancies (company is a User with role=company)
CREATE TABLE vacancies (
  vacancy_id   SERIAL PRIMARY KEY,
  company_id   UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  title        TEXT NOT NULL,
  description  TEXT NOT NULL,
  salary       NUMERIC,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- vacancy_skills (vacancy ↔ skill) importance 0..1, unique pair
CREATE TABLE vacancy_skills (
  id                 SERIAL PRIMARY KEY,
  vacancy_id         INTEGER NOT NULL REFERENCES vacancies(vacancy_id) ON DELETE CASCADE,
  skill_id           INTEGER NOT NULL REFERENCES skills(skill_id) ON DELETE CASCADE,
  importance_weight  NUMERIC(3,2) NOT NULL DEFAULT 1.00,
  CONSTRAINT ck_vacancy_skills_weight CHECK (importance_weight >= 0.00 AND importance_weight <= 1.00),
  CONSTRAINT uq_vacancy_skill UNIQUE (vacancy_id, skill_id)
);

-- student_skills (user ↔ skill) level 1..5, unique pair
CREATE TABLE student_skills (
  id        SERIAL PRIMARY KEY,
  user_id   UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  skill_id  INTEGER NOT NULL REFERENCES skills(skill_id) ON DELETE CASCADE,
  level     INTEGER NOT NULL,
  CONSTRAINT ck_student_level CHECK (level BETWEEN 1 AND 5),
  CONSTRAINT uq_student_skill UNIQUE (user_id, skill_id)
);

-- coverage_results (vacancy ↔ course) computed analytics
CREATE TABLE coverage_results (
  id               SERIAL PRIMARY KEY,
  vacancy_id       INTEGER NOT NULL REFERENCES vacancies(vacancy_id) ON DELETE CASCADE,
  course_id        INTEGER NOT NULL REFERENCES courses(course_id) ON DELETE CASCADE,
  coverage_percent NUMERIC(5,2) NOT NULL,
  missing_skills   JSONB NOT NULL DEFAULT '[]'::jsonb,
  created_at       TIMESTAMP NOT NULL DEFAULT NOW(),
  CONSTRAINT ck_coverage_percent CHECK (coverage_percent >= 0.00 AND coverage_percent <= 100.00),
  CONSTRAINT uq_vacancy_course UNIQUE (vacancy_id, course_id)
);

-- ---------- Helpful indexes ----------
CREATE INDEX IF NOT EXISTS ix_skills_name ON skills (name);
CREATE INDEX IF NOT EXISTS ix_vacancies_company ON vacancies (company_id);
CREATE INDEX IF NOT EXISTS ix_vacancy_skills_v ON vacancy_skills (vacancy_id);
CREATE INDEX IF NOT EXISTS ix_student_skills_user ON student_skills (user_id);

-- ---------- Seed data ----------

-- Fixed UUIDs so relations below are simple & repeatable
-- student user
INSERT INTO users (user_id, full_name, email, role)
VALUES ('11111111-1111-1111-1111-111111111111', 'Анастасия Студент', 'student@example.com', 'student');

-- company user
INSERT INTO users (user_id, full_name, email, role)
VALUES ('22222222-2222-2222-2222-222222222222', 'ООО Пример Тех', 'hr@company.example', 'company');

-- skills (3+)
INSERT INTO skills (name, category, description) VALUES
  ('python', 'backend', 'Язык программирования Python'),
  ('sql',    'database','Запросы к БД, реляционные основы'),
  ('docker', 'devops',  'Контейнеризация приложений');

-- courses (2)
INSERT INTO courses (title, description, provider, duration_hours, difficulty) VALUES
  ('Основы Python', 'Базовый курс по Python', 'БГУИР', 24, 'beginner'),
  ('БД и SQL',      'Реляционные модели и SQL', 'БГУИР', 20, 'beginner');

-- map courses ↔ skills
-- курс 1: Python (1.00)
INSERT INTO course_skills (course_id, skill_id, coverage_weight) VALUES
  (1, 1, 1.00),               -- Основы Python → python
  (2, 2, 1.00);               -- БД и SQL     → sql

-- vacancy by company (UUID 2222-...)
INSERT INTO vacancies (company_id, title, description, salary)
VALUES (
  '22222222-2222-2222-2222-222222222222',
  'Backend Intern',
  'Ищем стажёра backend: Python, SQL, Docker (желательно). Проекты на Django.',
  800
);

-- vacancy 1 required skills
INSERT INTO vacancy_skills (vacancy_id, skill_id, importance_weight) VALUES
  (1, 1, 1.00),  -- python (must)
  (1, 2, 1.00),  -- sql (must)
  (1, 3, 0.50);  -- docker (nice-to-have)

-- student has python/sql (no docker)
INSERT INTO student_skills (user_id, skill_id, level) VALUES
  ('11111111-1111-1111-1111-111111111111', 1, 3),  -- python lvl 3
  ('11111111-1111-1111-1111-111111111111', 2, 2);  -- sql lvl 2

-- example analytics (coverage results for vacancy 1 vs courses)
-- Допустим: курс "Основы Python" покрывает ~66.67% (из python/sql/docker покрывает python=1.0 из 1.0+1.0+0.5=2.5 → 40%,
-- но в демо поставим наглядные значения)
INSERT INTO coverage_results (vacancy_id, course_id, coverage_percent, missing_skills)
VALUES
  (1, 1, 66.67, '["sql","docker"]'),
  (1, 2, 66.67, '["python","docker"]');

COMMIT;
