from celery import shared_task, group
from celery.utils.log import get_task_logger
import logging

keys = ['auto', 'disability', 'home', 'life']


logger = get_task_logger(__name__)
# logger = logging.getLogger(__name__)


@shared_task
def age_rule(base, age=None, **kwargs):
    result = base.copy()
    if age and age > 60:
        result['disability'] = 'ineligible'
        logger.warning('ineligible for disability due age rule')
        result['life'] = 'ineligible'
        logger.warning('ineligible for life due age rule')

    return result


@shared_task
def income_rule(base, income=None, **kwargs):
    result = base.copy()
    if not income or income == 0:
        result['disability'] = 'ineligible'
        logger.warning('ineligible for disability due income rule')

    return result


@shared_task
def house_rule(base, house=None, **kwargs):
    result = base.copy()
    if not house:
        result['home'] = 'ineligible'
        logger.warning('ineligible for home due house rule')

    return result


@shared_task
def vehicle_rule(base, vehicle=None, **kwargs):
    result = base.copy()
    if not vehicle:
        result['auto'] = 'ineligible'
        logger.warning('ineligible for auto due vehicle rule')

    return result


rules = [
    age_rule,
    income_rule,
    house_rule,
    vehicle_rule,
]


def ineligible(base=None, **kwargs):
    if not base:
        base = {k: 0 for k in keys}

    for rule in rules:
        base = rule(base, **kwargs)

    return base


@shared_task
def agreggate_ineligible(values, base):
    result = base.copy()
    for item in values:
        for k, v in item.items():
            if v == 'ineligible':
                result[k] = v
    return result


@shared_task(bind=True)
def ineligible_async(self, base=None, **kwargs):
    zeros = {k: 0 for k in keys}

    task = group(
        rule.s(zeros, **kwargs) for rule in rules
    ) | agreggate_ineligible.s(base)

    return self.replace(task)
