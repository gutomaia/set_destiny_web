
class GradeRulesSpec:

    def when_grade_rule_with(self, **kwargs):
        raise NotImplementedError()

    def assert_grade(self, **kwargs):
        raise NotImplementedError()

    def test_grade_economic(self):
        self.when_grade_rule_with(home=0)

        self.assert_grade(home='economic')

    def test_grade_regular_with_1(self):
        self.when_grade_rule_with(home=1)

        self.assert_grade(home='regular')

    def test_grade_regular_with_2(self):
        self.when_grade_rule_with(home=2)

        self.assert_grade(home='regular')

    def test_grade_responsible(self):
        self.when_grade_rule_with(home=3)

        self.assert_grade(home='responsible')

    def test_grade_inaligible(self):
        self.when_grade_rule_with(home='ineligible')

        self.assert_grade(home='ineligible')

