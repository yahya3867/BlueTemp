"""
This file is the entry point of the Flask application.
It creates the Flask app and initializes the database and OAuth
"""

# flaskr/__init__.py

# Python Standard Library Imports
import os

# Python Third Party Imports
# This has to be created here to avoid circular imports
from flask import Flask
from flask_session import Session

# Local Library Imports
from lib.database import DatabaseService

from . import database
from .public import PUBLIC



def create_app():
    """
    Create the Flask app and configure it with the necessary settings

    Returns:
        Flask: The Flask app
    """
    # create and configure the app
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object("config.Config")

    app.jinja_env.autoescape = False

    app.jinja_env.globals["WEBSITE_NAME"] = app.config["WEBSITE_NAME"]
    app.jinja_env.globals["WEBSITE_EMAIL"] = app.config["WEBSITE_EMAIL"]
    app.jinja_env.globals["WEBSITE_LOGO"] = app.config["WEBSITE_LOGO"]

    # App session setup
    app_session = Session()
    app_session.init_app(app)
    #app.database_service = DatabaseService(app.config["SQLALCHEMY_DATABASE_URI"])

    # Initializing the database
    #database.init_app(app)

    # Registering the Blueprint APIs
    app.register_blueprint(PUBLIC)

    return app
