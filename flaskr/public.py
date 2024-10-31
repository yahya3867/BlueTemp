"""The blueprint API route for all public endpoints"""

# Python Third Party Imports
from flask import Blueprint, render_template


# Creating the blueprint route for Public
PUBLIC = Blueprint(name="public", import_name=__name__, template_folder="/templates")


@PUBLIC.route("/", methods=["GET", "POST"])
@PUBLIC.route("/home", methods=["GET", "POST"])
def homepage():
    """API ENDPOINT
    The endpoint for rendering the homepage

    Returns:
        render_template: Renders the homepage/home
        html
    """
    return render_template("homepage/base.html")