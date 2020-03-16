from unittest import TestCase
from set_destiny_web.test.score_rules_spec import ScoreRulesSpec
from set_destiny_web.risk import score


class ScoreTest(ScoreRulesSpec, TestCase):

    def setUp(self):
        self.base = {k: 0 for k in ['auto', 'disability', 'home', 'life']}
        self.score = {}

    def given_date(self, *args):
        pass

    def when_score_with(self, **kwargs):
        self.score = score.score(self.base, **kwargs)

    def __getattribute__(self, name):
        if name.endswith('_rule_with'):
            return self.when_score_with
        return super(ScoreTest, self).__getattribute__(name)

    def assert_score(self, **kwargs):
        for k, v in kwargs.items():
            self.assertIn(k, self.score)
            self.assertEqual(v, self.score[k])
