CREATE DATABASE edit;

CREATE TABLE courses (
  id              SERIAL PRIMARY KEY NOT NULL,
  title           TEXT NOT NULL,
  author          TEXT NOT NULL,
  contents        TEXT NOT NULL,
);