#!/usr/bin/python3

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from src.models.base import Base
from flask import current_app

config = context.config
config.set_main_option('sqlalchemy.url', current_app.config['SQLALCHEMY_DATABASE_URI'])

engine = engine_from_config(
    config.get_section(config.config_ini_section),
    prefix='sqlalchemy.',
    poolclass=pool.NullPool)

connection = engine.connect()
context.configure(
    connection=connection,
    target_metadata=Base.metadata
)

with context.begin_transaction():
    context.run_migrations()
