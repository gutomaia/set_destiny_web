from .web import HttpMixin


class ScoreMixin:

    def assert_score(self, **kwargs):
        for k, v in kwargs.items():
            self.assertIn(k, self.score, f'{k} not found in {self.score}')
            self.assertEqual(v, self.score[k], f'-- {k} shoud be {v} and it is {self.score[k]}')
