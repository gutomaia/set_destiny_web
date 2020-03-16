from unittest import TestCase
from set_destiny_web.test.ineligible_rules_spec import IneligibleRulesSpec
from set_destiny_web.risk import ineligible


class IneligibleTest(IneligibleRulesSpec, TestCase):

    def setUp(self):
        self.base = {k: 0 for k in ['auto', 'disability', 'home', 'life']}
        self.score = {}

    def given_date(self, *args):
        pass

    def when_score_with(self, **kwargs):
        self.score = ineligible.ineligible(self.base, **kwargs)

    def __getattribute__(self, name):
        if name.endswith('_rule_with'):
            return self.when_score_with
        return super(IneligibleTest, self).__getattribute__(name)

    def assert_score(self, **kwargs):
        for k, v in kwargs.items():
            self.assertIn(k, self.score)
            self.assertEqual(v, self.score[k])
