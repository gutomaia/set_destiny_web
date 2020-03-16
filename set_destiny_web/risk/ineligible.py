keys = ['auto', 'disability', 'home', 'life']


def age_rule(base, age=None, **kwargs):
    if age and age > 60:
        base['disability'] = 'ineligible'
        base['life'] = 'ineligible'

    return base


def income_rule(base, income=None, **kwargs):
    if not income or income == 0:
        base['disability'] = 'ineligible'

    return base


def house_rule(base, house=None, **kwargs):
    if not house:
        base['home'] = 'ineligible'

    return base


def vehicle_rule(base, vehicle=None, **kwargs):
    if not vehicle:
        base['auto'] = 'ineligible'

    return base


def ineligible(base=None, **kwargs):
    if not base:
        base = {k: 0 for k in keys}

    rules = [
        age_rule,
        income_rule,
        house_rule,
        vehicle_rule,
    ]

    for rule in rules:
        base = rule(base, **kwargs)

    return base
