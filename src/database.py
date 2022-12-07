"""Finsta Service Database"""
# Flask imports
from flask_sqlalchemy import SQLAlchemy
# Finsta imports
from finsta.src.app import app

# Create DB
db = SQLAlchemy(app)
