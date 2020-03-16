from unittest import TestCase
from set_destiny_web.test.profile_spec import ProfileSpec
from set_destiny_web.test.mixins.web import HttpMixin

from flask import Flask
from set_destiny_web.api import api
import json


class ProfileTest(HttpMixin, ProfileSpec, TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(api, url_prefix='/api')

        self.client = self.app.test_client()

    def when_post_profile(self, **kwargs):
        self.response = self.client.post('/api/profile/',
                                         data=json.dumps(kwargs),
                                         content_type='application/json',)
