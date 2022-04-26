from json.decoder import JSONDecodeError
import logging
import unittest
from urllib.parse import urlencode

import oauthlib.oauth1
import flask
from flask import Flask, url_for
import flask_testing
import requests_mock
from pylti.common import LTI_SESSION_KEY
import time

from mock import patch, mock_open
import views


@requests_mock.Mocker()
class LTITests(flask_testing.TestCase):
    def create_app(self):
        app = views.app
        app.config["PRESERVE_CONTEXT_ON_EXCEPTION"] = False
        app.config["SECRET_KEY"] = "S3cr3tK3y"
        app.config["SESSION_COOKIE_DOMAIN"] = None

        return app

    @classmethod
    def setUpClass(cls):
        logging.disable(logging.CRITICAL)
        app = views.app
        app.config["BASE_URL"] = "https://example.edu/"
        app.config["GOOGLE_ANALYTICS"] = "123abc"

    def setUp(self):
        with self.app.test_request_context():
            pass

    @classmethod
    def tearDownClass(cls):
        logging.disable(logging.NOTSET)

    def tearDown(self):
        pass

    @staticmethod
    def generate_launch_request(
        url,
        body=None,
        http_method="GET",
        base_url="http://localhost",
        roles="Instructor",
        headers=None,
    ):
        params = {}

        if roles is not None:
            params["roles"] = roles

        urlparams = urlencode(params)

        client = oauthlib.oauth1.Client(
            "CHANGEME",
            client_secret="CHANGEME",
            signature_method=oauthlib.oauth1.SIGNATURE_HMAC,
            signature_type=oauthlib.oauth1.SIGNATURE_TYPE_QUERY,
        )
        signature = client.sign(
            "{}{}?{}".format(base_url, url, urlparams),
            body=body,
            http_method=http_method,
            headers=headers,
        )
        signed_url = signature[0]
        new_url = signed_url[len(base_url) :]
        return new_url


    # index
    def test_index(self, m):
        response = self.client.get(url_for("index"))

        self.assert_200(response)
        self.assert_template_used("index.html")

        self.assertIn(
            b"LTI Python/Flask Template", response.data
        )

    # xml
    def test_xml(self, m):
        response = self.client.get(url_for("xml"))

        self.assert_200(response)
        self.assert_template_used("lti.xml")
        self.assertEqual(response.mimetype, "application/xml")


    # launch
    def test_launch(self, m):
        with self.client.session_transaction() as sess:
            sess[LTI_SESSION_KEY] = True
            sess["oauth_consumer_key"] = "key"
            sess["roles"] = "Instructor"
            sess["canvas_user_id"] = 1
            sess["user_id"] = 1

        payload = {
            "launch_presentation_return_url": "http://localhost/",
            "custom_canvas_user_id": "1",
            "custom_canvas_course_id": "1",
            "user_id": "1",
            "lis_person_name_full": "Tester",
        }

        signed_url = self.generate_launch_request(
            "/launch",
            http_method="POST",
            body=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        response = self.client.post(
            signed_url,
            data=payload,
        )

        self.assertIn(b"Tester", response.data)
        self.assert_200(response)
        self.assert_template_used("launch.html")

    # error launch
    def test_error(self, m):
        response = self.client.get(url_for("launch"))

        self.assert_200(response)
        self.assert_template_used("error.html")

