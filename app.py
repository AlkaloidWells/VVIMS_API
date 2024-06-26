from flask.json import jsonify
from constants.http_status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from flask import Flask, config, redirect
import os
from api.auth import auth
from api.company import company
from api.employee import employee 
from api.visitor import visitor
from api.vircul import vircul
from api.comp_user import user1
from api.sadmin import sadmin
from model.models import db, init_db
from flask_jwt_extended import JWTManager
from flasgger import Swagger, swag_from
from config.swaga import template, swagger_config

basedir = os.path.abspath(os.path.dirname(__file__))

test_config=None
app = Flask(__name__, instance_relative_config=True)


if test_config is None:
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db', 'vvims.db'),
        SECRET_KEY = '8IR4M7-R3c74GjTHhKzWODaYVHuPGqn4w92DHLqeYJA',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY='8IR4M7-R3c74GjTHhKzWODaYVHuPGqn4w92DHLqeYJA',

        SWAGGER={
            'title': "VVIMS API",
            'uiversion': 3
        }
    )
else:
    app.config.from_mapping(test_config)

db.init_app(app)

#with app.app_context():
    #init_db()
    
JWTManager(app)
app.register_blueprint(auth)
app.register_blueprint(company)
app.register_blueprint(employee)
app.register_blueprint(visitor)
app.register_blueprint(vircul)
app.register_blueprint(user1)
app.register_blueprint(sadmin)


Swagger(app, config=swagger_config, template=template)

@app.errorhandler(HTTP_404_NOT_FOUND)
def handle_404(e):
    return jsonify({'error': 'Not found'}), HTTP_404_NOT_FOUND

@app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
def handle_500(e):
    return jsonify({'error': 'Something went wrong, we are working on it'}), HTTP_500_INTERNAL_SERVER_ERROR


    return app

if __name__ == '__main__':
    app.run(debug=True)

