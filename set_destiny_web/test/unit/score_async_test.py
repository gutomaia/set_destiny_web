from unittest import TestCase
from unittest.mock import patch
from set_destiny_web.test.score_rules_spec import ScoreRulesSpec
from set_destiny_web.risk import score
from celery import Celery


class ScoreAsyncTest(ScoreRulesSpec, TestCase):

    def score_async_replace_wraps(self, chord):
        eager_result = chord.delay()
        self.score = eager_result.result
        return self.score

    def setUp(self):
        self.base = {k: 0 for k in ['auto', 'disability', 'home', 'life']}
        self.score = {}
        self.celery = Celery()
        self.celery.conf.task_always_eager = True

        self.score_async_replace_patch = patch('set_destiny_web.risk.score.score_async.replace',
                                               wraps=self.score_async_replace_wraps)

        self.score_async_replace = self.score_async_replace_patch.start()

    def tearDown(self):
        self.score_async_replace_patch.stop()

    def given_date(self, *args):
        pass

    def when_score_with(self, **kwargs):
        score.score_async.s(self.base, **kwargs).delay()

    def __getattribute__(self, name):
        if name.endswith('_rule_with'):
            return self.when_score_with
        return super(ScoreAsyncTest, self).__getattribute__(name)

    def assert_score(self, **kwargs):
        for k, v in kwargs.items():
            self.assertIn(k, self.score)
            self.assertEqual(v, self.score[k])
