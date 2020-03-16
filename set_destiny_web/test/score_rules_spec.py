

class ScoreRulesSpec:

    def given_date(self, *args):
        raise NotImplementedError()

    def when_base_rule_with(self, **kwargs):
        raise NotImplementedError()

    def when_age_rule_with(self, **kwargs):
        raise NotImplementedError()

    def when_income_rule_with(self, **kwargs):
        raise NotImplementedError()

    def when_house_rule_with(self, **kwargs):
        raise NotImplementedError()

    def when_dependents_rule_with(self, **kwargs):
        raise NotImplementedError()

    def when_married_rule_with(self, **kwargs):
        raise NotImplementedError()

    def when_vehicle_rule_with(self, **kwargs):
        raise NotImplementedError()

    def assert_score(self, **kwargs):
        raise NotImplementedError()

    def test_score_base_home_1(self):
        self.when_base_rule_with(risk_questions=[0, 0, 1])

        self.assert_score(home=1)

    def test_score_base_life_3(self):
        self.when_base_rule_with(risk_questions=[1, 1, 1])

        self.assert_score(life=3)

    def test_score_age_lower_30_deduct_2(self):
        self.when_age_rule_with(age=29)

        self.assert_score(
            auto=-2,
            disability=-2,
            home=-2,
            life=-2)

    def test_score_age_between_30_and_40_deduct_1(self):
        self.when_age_rule_with(age=35)

        self.assert_score(
            auto=-1,
            disability=-1,
            home=-1,
            life=-1)

    def test_score_income_over_200k_deduct_1(self):
        self.when_income_rule_with(income=200_001)

        self.assert_score(
            auto=-1,
            disability=-1,
            home=-1,
            life=-1)

    def test_score_home_mortgaged_add_1_to_disability_and_home(self):
        self.when_house_rule_with(house=dict(ownership_status='mortgaged'))

        self.assert_score(
            auto=0,
            disability=1,
            home=1,
            life=0)

    def test_score_home_owned_dont_add(self):
        self.when_house_rule_with(house=dict(ownership_status='owned'))

        self.assert_score(
            auto=0,
            disability=0,
            home=0,
            life=0)

    def test_score_dependents_add_1_to_disability_and_life(self):
        self.when_dependents_rule_with(dependents=1)

        self.assert_score(
            auto=0,
            disability=1,
            home=0,
            life=1)

    def test_score_married_add_1_to_life_and_remove_1_from_disability(self):
        self.when_married_rule_with(marital_status='married')

        self.assert_score(
            auto=0,
            disability=-1,
            home=0,
            life=1)

    def test_score_vehicle_newer_than_5_years_add_1_auto(self):
        self.given_date(2020, 2, 1)

        self.when_vehicle_rule_with(vehicle=dict(year=2018))

        self.assert_score(
            auto=1,
            disability=0,
            home=0,
            life=0
        )

    def test_score_vehicle_older_than_5_years_do_nothing(self):
        self.given_date(2020, 2, 1)

        self.when_vehicle_rule_with(vehicle=dict(year=2013))

        self.assert_score(
            auto=0,
            disability=0,
            home=0,
            life=0
        )
