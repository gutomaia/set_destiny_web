from unittest import TestCase
from unittest.mock import patch
from set_destiny_web.test.ineligible_rules_spec import IneligibleRulesSpec
from set_destiny_web.risk import ineligible
from celery import Celery


class IneligibleAsyncTest(IneligibleRulesSpec, TestCase):

    def ineligible_async_replace_wraps(self, chord):
        eager_result = chord.delay()
        self.score = eager_result.result
        return self.score

    def setUp(self):
        self.base = {k: 0 for k in ['auto', 'disability', 'home', 'life']}
        self.score = {}
        self.celery = Celery()
        self.celery.conf.task_always_eager = True

        self.ineligible_async_replace_patch = patch('set_destiny_web.risk.ineligible.ineligible_async.replace',
                                                    wraps=self.ineligible_async_replace_wraps)

        self.ineligible_async_replace = self.ineligible_async_replace_patch.start()

    def tearDown(self):
        self.ineligible_async_replace_patch.stop()

    def given_date(self, *args):
        pass

    def when_score_with(self, **kwargs):
        ineligible.ineligible_async.s(self.base, **kwargs).delay()

    def __getattribute__(self, name):
        if name.endswith('_rule_with'):
            return self.when_score_with
        return super(IneligibleAsyncTest, self).__getattribute__(name)

    def assert_score(self, **kwargs):
        for k, v in kwargs.items():
            self.assertIn(k, self.score)
            self.assertEqual(v, self.score[k])
