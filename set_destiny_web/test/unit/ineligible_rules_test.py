from unittest import TestCase
from set_destiny_web.test.ineligible_rules_spec import IneligibleRulesSpec
from set_destiny_web.risk import ineligible


class IneligibleRulesTest(IneligibleRulesSpec, TestCase):

    def setUp(self):
        self.base = {k: 0 for k in ['auto', 'disability', 'home', 'life']}
        self.score = {}

    def when_age_rule_with(self, **kwargs):
        self.score = ineligible.age_rule(self.base, **kwargs)

    def when_income_rule_with(self, **kwargs):
        self.score = ineligible.income_rule(self.base, **kwargs)

    def when_house_rule_with(self, **kwargs):
        self.score = ineligible.house_rule(self.base, **kwargs)

    def when_vehicle_rule_with(self, **kwargs):
        self.score = ineligible.vehicle_rule(self.base, **kwargs)

    def assert_score(self, **kwargs):
        for k, v in kwargs.items():
            self.assertIn(k, self.score)
            self.assertEqual(v, self.score[k])
