from flask_restplus import Namespace, Resource, fields
from set_destiny_web.risk.score import score
from set_destiny_web.risk.ineligible import ineligible
from set_destiny_web.risk.grade import grade
from set_destiny_web.background.tasks import calculate_risk


import enum


ns = Namespace('profile', description='Profile related operations')


class HouseOwnershipStatus(enum.Enum):
    owned = 'owned'
    mortgaged = 'mortgaged'


class MaritalStatus(enum.Enum):
    single = 'single'
    married = 'married'


house_fields = {
    'ownership_status': fields.String(description='Ownership status',
                                      enum=HouseOwnershipStatus._member_names_)
}

house = ns.model('House', house_fields)

vehicle_fields = {
    'year': fields.Integer(required=True, description='Year')
}

vehicle = ns.model('Vehicle', vehicle_fields)


profile_fields = {
    'age': fields.Integer(required=True, description='Age'),
    'dependents': fields.Integer(required=True, description='Dedependents'),
    'house': fields.Nested(house, required=False),
    'income': fields.Integer(required=False, description='Income'),
    'marital_status': fields.String(required=True,
                                    description='Marital status',
                                    enum=MaritalStatus._member_names_),
    'risk_questions': fields.List(fields.Integer,
                                  required=True,
                                  min_items=3,
                                  max_items=3,
                                  description='Risk questions'),
    'vehicle': fields.Nested(vehicle, required=False),
}


profile = ns.model('Profile', profile_fields)


ECONOMIC = 'economic'
REGULAR = 'regular'
RESPONSIBLE = 'responsible'
INELIGIBLE = 'ineligible'


class Insurance(enum.Enum):
    economic = ECONOMIC
    regular = REGULAR
    responsible = RESPONSIBLE
    ineligible = INELIGIBLE


insurance_fields = {
    'auto': fields.String(description='auto', enum=Insurance._member_names_),
    'disability': fields.String(description='disability', enum=Insurance._member_names_),
    'home': fields.String(description='home', enum=Insurance._member_names_),
    'life': fields.String(description='life', enum=Insurance._member_names_),
}


insurance = ns.model('Insurance', insurance_fields)


@ns.route('/')
class ProfileList(Resource):

    @ns.doc(description='create profile')
    @ns.expect(profile)
    @ns.marshal_with(insurance, code=201)
    def post(self):
        scores = score(**ns.payload)
        elegiblity = ineligible(scores, **ns.payload)
        data = grade(elegiblity)

        return data, 201


@ns.route('/async')
class ProfileAsync(Resource):

    @ns.doc(description='create profile async')
    @ns.expect(profile)
    @ns.marshal_with(insurance, code=202)
    def post(self):
        calculate_risk.s(**ns.payload).apply_async()

        return dict(status='Accepted'), 202
