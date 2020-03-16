from flask import Flask, url_for
from set_destiny_web.api import api
from flask_restplus import apidoc
from os.path import dirname, join


custom_apidoc = apidoc.Apidoc('restplus_custom_doc', __name__,
                              template_folder='templates',
                              static_folder=join(dirname(apidoc.__file__), 'static'),
                              static_url_path='swaggerui')


@custom_apidoc.add_app_template_global
def swagger_static(filename):
    return url_for('restplus_doc.static', filename=filename)


def create_app():
    app = Flask(__name__)
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(custom_apidoc, url_prefix='/api')

    return app
