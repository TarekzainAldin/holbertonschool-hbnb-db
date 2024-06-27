-- 02_create_country_table.sql

CREATE TABLE countries (
    code VARCHAR(36) PRIMARY KEY,
    name VARCHAR(128) NOT NULL
);
