

class HttpMixin:

    def assert_status(self, status):
        self.assertEqual(status, self.response.status_code)

    def assert_ok(self):
        self.assert_status(200)

    def assert_created(self):
        self.assert_status(201)

    def assert_bad_request(self):
        self.assert_status(400)

    def assert_response(self, **kwargs):
        data = self.response.json
        for k, v in kwargs.items():
            self.assertIn(k, data)
            self.assertEqual(v, data[k])
