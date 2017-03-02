from flask import Flask, render_template, session, request, Response, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from datetime import timedelta
from pylti.flask import lti
import settings
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.secret_key = settings.secret_key
app.config.from_object(settings.configClass)
db = SQLAlchemy(app)


# ============================================
# Logging
# ============================================

formatter = logging.Formatter(settings.LOG_FORMAT)
handler = RotatingFileHandler(
    settings.LOG_FILE,
    maxBytes=settings.LOG_MAX_BYTES,
    backupCount=settings.LOG_BACKUP_COUNT
)
handler.setLevel(logging.getLevelName(settings.LOG_LEVEL))
handler.setFormatter(formatter)
app.logger.addHandler(handler)

# ============================================
# DB Model Example
# ============================================


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    special_key = db.Column(db.String)

    def __init__(self, user_id, special_key):
        self.user_id = user_id
        self.special_key = special_key

    def __repr__(self):
        return '<User %r>' % self.user_id


# ============================================
# Utility Functions
# ============================================

def return_error(msg):
    return render_template('error.htm.j2', msg=msg)


def error(exception=None):
    app.logger.error("PyLTI error: {}".format(exception))
    return return_error('''Authentication error,
        please refresh and try again. If this error persists,
        please contact support.''')


# ============================================
# Web Views / Routes
# ============================================


@app.route('/launch', methods=['POST', 'GET'])
@lti(error=error, request='initial', role='any', app=app)
def launch(lti=lti):
    # examples of getting data from the form
    session['course_id'] = request.form.get('custom_canvas_course_id')
    session['user_id'] = request.form.get('custom_canvas_user_id')

    return redirect(url_for('post_launch'))


@app.route('/post_launch', methods=['POST', 'GET'])
@lti(error=error, request='session', role='any', app=app)
def post_launch(lti=lti):
    msg = "Heya, the course ID is {}. The user is {}.".format(
        session['course_id'], session['user_id']
    )
    return render_template('index.htm.j2', msg=msg)


@app.route('/', methods=['GET'])
@lti(error=error, request='any', role='any', app=app)
def index(lti=lti):
    return return_error('Please contact your System Administrator.')


# ============================================
# XML
# ============================================

@app.route("/xml/", methods=['GET'])
def xml():
    """
    Returns the lti.xml file for the app.
    XML can be built at https://www.eduappcenter.com/
    """
    try:
        return Response(render_template(
            'lti.xml.j2'), mimetype='application/xml'
        )
    except:
        app.logger.error("Error with XML.")
        return return_error('''Error with XML. Please refresh and try again. If this error persists,
            please contact support.''')
