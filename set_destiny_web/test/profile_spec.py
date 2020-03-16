
class ProfileSpec:

    def when_post_profile(self, **kwargs):
        raise NotImplementedError()

    def assert_ok(self):
        raise NotImplementedError()

    def assert_created(self):
        raise NotImplementedError()

    def assert_response(self, **kwargs):
        raise NotImplementedError()

    def assert_score(self, **kwargs):
        raise NotImplementedError()

    def test_default_profile(self):
        self.when_post_profile(
            age=35,
            dependents=2,
            house={'ownership_status': 'owned'},
            income=1200,
            marital_status="married",
            risk_questions=[0, 1, 0],
            vehicle={'year': 2018})

        self.assert_created()

    def test_no_income_then_is_disability_ineligible(self):
        self.when_post_profile(
            income=0
        )

        self.assert_response(disability='ineligible')

    def test_no_vehicle_then_is_auto_ineligible(self):
        self.when_post_profile(
            vehicle=None
        )

        self.assert_response(auto='ineligible')

    def test_no_house_then_is_home_ineligible(self):
        self.when_post_profile(
            house=None
        )

        self.assert_response(home='ineligible')

    def test_user_over_60_years_is_ineligible_for_disability(self):
        self.when_post_profile(
            age=61
        )
        self.assert_response(disability='ineligible')

    def test_user_over_60_years_is_ineligible_for_life(self):
        self.when_post_profile(
            age=61
        )
        self.assert_response(life='ineligible')
