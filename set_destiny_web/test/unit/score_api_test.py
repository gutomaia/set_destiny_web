from unittest import TestCase
from unittest.mock import patch
from set_destiny_web.test.score_rules_spec import ScoreRulesSpec
from flask import Flask
from set_destiny_web.api import api
from set_destiny_web.risk.score import score as real_score
import json


class ScoreApiTest(ScoreRulesSpec, TestCase):

    def spy_score(self, **kwargs):
        self.score = real_score(**kwargs)
        return self.score

    def setUp(self):
        self.payload = dict(
            age=45,
            dependents=0,
            house={'ownership_status': 'owned'},
            income=1200,
            marital_status="single",
            risk_questions=[0, 0, 0],
            vehicle={'year': 2000}
        )
        self.score = {}
        self.score_patch = patch('set_destiny_web.api.profile.score', wraps=self.spy_score)
        self.score_mock = self.score_patch.start()
        self.app = Flask(__name__)
        self.app.register_blueprint(api, url_prefix='/api')

        self.client = self.app.test_client()

    def tearDown(self):
        self.score_patch.stop()

    def given_date(self, *args):
        pass

    def when_score_with(self, **kwargs):
        self.payload.update(kwargs)
        self.response = self.client.post('/api/profile/',
                                         data=json.dumps(self.payload),
                                         content_type='application/json',)

    def __getattribute__(self, name):
        if name.endswith('_rule_with'):
            return self.when_score_with
        return super(ScoreApiTest, self).__getattribute__(name)

    def assert_score(self, **kwargs):
        for k, v in kwargs.items():
            self.assertIn(k, self.score)
            self.assertEqual(v, self.score[k])
