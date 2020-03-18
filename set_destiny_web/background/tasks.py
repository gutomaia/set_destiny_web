from celery import shared_task
from set_destiny_web.risk.score import score_async as score
from set_destiny_web.risk.ineligible import ineligible_async as ineligible
from set_destiny_web.risk.grade import grade


@shared_task(bind=True)
def calculate_risk(self, base, **kwargs):
    workflow = (
        score.s(base, **kwargs) |
        ineligible.s(**kwargs) |
        grade.s()
    )

    return workflow.apply_async()
