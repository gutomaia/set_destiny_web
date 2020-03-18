from unittest import TestCase
from set_destiny_web.test.grade_rules_spec import GradeRulesSpec
from set_destiny_web.risk.grade import grade


class GradeRuleTest(GradeRulesSpec, TestCase):

    def when_grade_rule_with(self, **kwargs):
        self.grade = grade(kwargs)

    def assert_grade(self, **kwargs):
        for k, v in kwargs.items():
            self.assertIn(k, self.grade)
            self.assertEqual(v, self.grade[k])
