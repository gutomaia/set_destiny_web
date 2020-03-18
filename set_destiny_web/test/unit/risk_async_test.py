from unittest import TestCase
from unittest.mock import patch
from celery import Celery
from set_destiny_web.test.score_rules_spec import ScoreRulesSpec
from set_destiny_web.test.ineligible_rules_spec import IneligibleRulesSpec

from set_destiny_web.test.mixins import ScoreMixin

from set_destiny_web.background.tasks import calculate_risk


class RiskAsyncTest(ScoreMixin, IneligibleRulesSpec, ScoreRulesSpec, TestCase):

    def replace_wraps(self, chord):
        eager_result = chord.delay()
        self.score = eager_result.result
        return self.score

    def setUp(self):
        self.base = {k: 0 for k in ['auto', 'disability', 'home', 'life']}
        self.score = {}
        self.celery = Celery()
        self.celery.conf.task_always_eager = True

        self.score_async_replace_patch = patch('set_destiny_web.risk.score.score_async.replace',
                                               wraps=self.replace_wraps)

        self.score_async_replace = self.score_async_replace_patch.start()

        self.ineligible_async_replace_patch = patch('set_destiny_web.risk.ineligible.ineligible_async.replace',
                                                    wraps=self.replace_wraps)

        self.ineligible_async_replace = self.ineligible_async_replace_patch.start()

    def tearDown(self):
        self.score_async_replace_patch.stop()
        self.ineligible_async_replace_patch.stop()

    def given_date(self, *args):
        pass

    def when_score_with(self, **kwargs):
        default = dict(
            age=45,
            dependents=0,
            house={'ownership_status': 'owned'},
            income=1200,
            marital_status="single",
            risk_questions=[0, 0, 0],
            vehicle={'year': 2000}
        )

        default.update(kwargs)

        calculate_risk.s(self.base, **default).delay()

    def __getattribute__(self, name):
        if name.endswith('_rule_with'):
            return self.when_score_with
        return super(RiskAsyncTest, self).__getattribute__(name)
