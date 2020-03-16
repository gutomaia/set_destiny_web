

class IneligibleRulesSpec:

    def when_age_rule_with(self, **kwargs):
        raise NotImplementedError()

    def when_income_rule_with(self, **kwargs):
        raise NotImplementedError()

    def when_house_rule_with(self, **kwargs):
        raise NotImplementedError()

    def when_vehicle_rule_with(self, **kwargs):
        raise NotImplementedError()

    def test_no_income_then_is_disability_ineligible(self):
        self.when_income_rule_with(income=0)

        self.assert_score(disability='ineligible')

    def test_no_vehicle_then_is_auto_ineligible(self):
        self.when_vehicle_rule_with(vehicle=None)

        self.assert_score(auto='ineligible')

    def test_no_house_then_is_home_ineligible(self):
        self.when_house_rule_with(house=None)

        self.assert_score(home='ineligible')

    def test_user_over_60_years_is_ineligible_for_disability(self):
        self.when_age_rule_with(age=61)

        self.assert_score(disability='ineligible')

    def test_user_over_60_years_is_ineligible_for_life(self):
        self.when_age_rule_with(age=61)

        self.assert_score(life='ineligible')
