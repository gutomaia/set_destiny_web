from flask import Blueprint
from flask_restplus import Api
from .profile import ns as profile_ns


api = Blueprint('api', __name__)
api_def = Api(api,
              title='set destiny api',
              version='1.0',
              description='Reach there',
              )

api_def.add_namespace(profile_ns)
