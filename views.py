import os
import sys
from flask import Flask, render_template, session, request, Response
from pylti.flask import lti
import logging
import json
from logging import Formatter, INFO

app = Flask(__name__)
app.config.from_object(os.environ.get("CONFIG", "config.DevelopmentConfig"))
app.secret_key = app.config["SECRET_FLASK"]


# ============================================
# Logging
# ============================================

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(INFO)
handler.setFormatter(
    Formatter(
        "%(asctime)s %(levelname)s: %(message)s "
        "[in %(pathname)s: %(lineno)d of %(funcName)s]"
    )
)
app.logger.addHandler(handler)

# ============================================
# Utility Functions
# ============================================


def return_error(msg):
    return render_template("error.html", msg=msg)


def error(exception=None):
    app.logger.error("PyLTI error: {}".format(exception))
    return return_error(
        """Authentication error,
        please refresh and try again. If this error persists,
        please contact support."""
    )


# ============================================
# Web Views / Routes
# ============================================

# LTI Launch
@app.route("/launch", methods=["POST", "GET"])
@lti(error=error, request="initial", role="any", app=app)
def launch(lti=lti):
    """
    Returns the launch page
    request.form will contain all the lti params
    """

    # example of getting lti data from the request
    # let's just store it in our session
    session["lis_person_name_full"] = request.form.get("lis_person_name_full")

    # Write the lti params to the console
    app.logger.info(json.dumps(request.form, indent=2))

    return render_template(
        "launch.html", lis_person_name_full=session["lis_person_name_full"]
    )


# Home page
@app.route("/", methods=["GET"])
def index(lti=lti):
    return render_template("index.html")


# LTI XML Configuration
@app.route("/xml/", methods=["GET"])
def xml():
    """
    Returns the lti.xml file for the app.
    XML can be built at https://www.eduappcenter.com/
    """
    return Response(render_template("lti.xml"), mimetype="application/xml")
