import os


class BaseConfig(object):
    DEBUG = False
    TESTING = False

    # Using a placeholder for environment variables.
    # If not found in the environment, it will default to the local value, which is set in
    # the second parameter. Example:
    # os.environ.get("ENVIRONMENT_KEY", "LOCAL_VALUE")
    # This makes it a bit easier to use one file for local and environment deployment.

    # Declare your consumer key and shared secret. If you end
    # up having multiple consumers, you may want to add separate
    # key/secret sets for them.
    CONSUMER_KEY = os.environ.get("CONSUMER_KEY", "CHANGEME")
    SHARED_SECRET = os.environ.get("SHARED_SECRET", "CHANGEME")

    # Configuration for LTI
    PYLTI_CONFIG = {
        "consumers": {
            CONSUMER_KEY: {"secret": SHARED_SECRET}
            # Feel free to add more key/secret pairs for other consumers.
        },
        "roles": {
            # Maps values sent in the lti launch value of "roles" to a group
            # Allows you to check LTI.is_role('admin') for your user
            "admin": ["Administrator", "urn:lti:instrole:ims/lis/Administrator"],
            "student": ["Student", "urn:lti:instrole:ims/lis/Student"],
        },
    }

    # Secret key used for Flask sessions, etc. Must stay named 'secret_key'.
    # Can be any randomized string, recommend generating one with os.urandom(24)
    secret_key = os.environ.get("SECRET_FLASK", "CHANGEME")
    SECRET_FLASK = os.environ.get("SECRET_FLASK", "CHANGEME")
    # Store application wide settings here
    # For example: we could store our app's api keys for canvas
    #
    # CANVAS_API_URL = ''
    # CANVAS_API_KEY = ''
    #


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True


# DEFINE ADDITIONAL CONFIGS AS NEEDED
