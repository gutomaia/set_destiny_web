from celery import shared_task, group
from datetime import datetime


keys = ['auto', 'disability', 'home', 'life']


@shared_task
def base_rule(base, risk_questions=None, **kwargs):
    total = sum(risk_questions) if risk_questions else 0

    result = base.copy()
    for k in keys:
        result[k] += total

    return result


@shared_task
def age_rule(base, age=None, **kwargs):
    deduct = 0
    if age:
        if age < 30:
            deduct = -2
        elif age < 40:
            deduct = -1

    result = base.copy()
    for k in keys:
        result[k] += deduct

    return result


@shared_task
def income_rule(base, income=None, **kwargs):
    deduct = 0

    if income and income > 200_000:
        deduct = -1

    result = base.copy()
    for k in keys:
        result[k] += deduct

    return result


@shared_task
def house_rule(base, house=None, **kwargs):
    result = base.copy()
    if house and house['ownership_status'] == 'mortgaged':
        for k in ['home', 'disability']:
            result[k] += 1

    return result


@shared_task
def dependents_rule(base, dependents=None, **kwargs):
    result = base.copy()
    if dependents and dependents > 0:
        for k in ['disability', 'life']:
            result[k] += 1

    return result


@shared_task
def married_rule(base, marital_status=None, **kwargs):
    result = base.copy()
    if marital_status and marital_status == 'married':
        result['disability'] -= 1
        result['life'] += 1

    return result


@shared_task
def vehicle_rule(base, vehicle=None, **kwargs):
    result = base.copy()
    now = datetime.now()
    if vehicle and (now.year - vehicle.get('year', 0)) < 5:
        result['auto'] += 1

    return result


rules = [
    base_rule,
    age_rule,
    income_rule,
    house_rule,
    dependents_rule,
    married_rule,
    vehicle_rule,
]


def score(base=None, **kwargs):
    if not base:
        base = {k: 0 for k in keys}

    for rule in rules:
        base = rule(base, **kwargs)

    return base


@shared_task
def sum_total(values, base):
    total = {}
    for v in values:
        for k, v in v.items():
            total[k] = total.get(k, 0) + v

    return total


@shared_task(bind=True)
def score_async(self, base=None, **kwargs):
    zeros = {k: 0 for k in keys}

    task = group(
        rule.s(zeros, **kwargs) for rule in rules
    ) | sum_total.s(base)

    return self.replace(task)
