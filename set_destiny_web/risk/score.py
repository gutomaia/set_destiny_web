from datetime import datetime

keys = ['auto', 'disability', 'home', 'life']


def base_rule(base, risk_questions=None, **kwargs):
    total = sum(risk_questions) if risk_questions else 0

    for k in keys:
        base[k] += total

    return base


def age_rule(base, age=None, **kwargs):
    deduct = 0
    if age:
        if age < 30:
            deduct = -2
        elif age < 40:
            deduct = -1

    for k in keys:
        base[k] += deduct

    return base


def income_rule(base, income=None, **kwargs):
    deduct = 0

    if income and income > 200_000:
        deduct = -1

    for k in keys:
        base[k] += deduct

    return base


def house_rule(base, house=None, **kwargs):
    if house and house['ownership_status'] == 'mortgaged':
        for k in ['home', 'disability']:
            base[k] += 1

    return base


def dependents_rule(base, dependents=None, **kwargs):
    if dependents and dependents > 0:
        for k in ['disability', 'life']:
            base[k] += 1

    return base


def married_rule(base, marital_status=None, **kwargs):
    if marital_status and marital_status == 'married':
        base['disability'] -= 1
        base['life'] += 1

    return base


def vehicle_rule(base, vehicle=None, **kwargs):
    now = datetime.now()
    if vehicle and (now.year - vehicle.get('year', 0)) < 5:
        base['auto'] += 1

    return base


def score(base=None, **kwargs):
    if not base:
        base = {k: 0 for k in keys}

    rules = [
        base_rule,
        age_rule,
        income_rule,
        house_rule,
        dependents_rule,
        married_rule,
        vehicle_rule,
    ]

    for rule in rules:
        base = rule(base, **kwargs)

    return base
