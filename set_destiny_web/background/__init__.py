from celery import Celery


def create_celery():
    app = Celery('worker')

    app.autodiscover_tasks(['set_destiny_web.background.tasks',
                            'set_destiny_web.risk.grade',
                            'set_destiny_web.risk.ineligible',
                            'set_destiny_web.risk.score',
                            ])

    return app
