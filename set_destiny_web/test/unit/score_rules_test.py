from unittest import TestCase
from set_destiny_web.test.score_rules_spec import ScoreRulesSpec
from set_destiny_web.risk import score


class ScoreRulesTest(ScoreRulesSpec, TestCase):

    def setUp(self):
        self.base = {k: 0 for k in ['auto', 'disability', 'home', 'life']}
        self.score = {}

    def given_date(self, *args):
        pass

    def when_base_rule_with(self, **kwargs):
        self.score = score.base_rule(self.base, **kwargs)

    def when_age_rule_with(self, **kwargs):
        self.score = score.age_rule(self.base, **kwargs)

    def when_income_rule_with(self, **kwargs):
        self.score = score.income_rule(self.base, **kwargs)

    def when_house_rule_with(self, **kwargs):
        self.score = score.house_rule(self.base, **kwargs)

    def when_dependents_rule_with(self, **kwargs):
        self.score = score.dependents_rule(self.base, **kwargs)

    def when_married_rule_with(self, **kwargs):
        self.score = score.married_rule(self.base, **kwargs)

    def when_vehicle_rule_with(self, **kwargs):
        self.score = score.vehicle_rule(self.base, **kwargs)

    def assert_score(self, **kwargs):
        for k, v in kwargs.items():
            self.assertIn(k, self.score)
            self.assertEqual(v, self.score[k])
