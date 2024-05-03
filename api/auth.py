from os import access
from constants.http_status_codes import (HTTP_200_OK, HTTP_201_CREATED, 
                                         HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, 
                                         HTTP_409_CONFLICT, HTTP_404_NOT_FOUND, 
                                         HTTP_204_NO_CONTENT)
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import validators
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from model.models import User, db
from utilites.checks import  role_allowed
from flasgger import Swagger, swag_from

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")



@auth.post('/register')
@swag_from('../docs/auth/register.yaml')
def register():
    username = request.json['username']
    email = request.json['email']
    role = request.json['role']
    password = request.json['password']

    if len(password) < 6:
        return jsonify({'error': "Password is too short"}), HTTP_400_BAD_REQUEST

    if len(username) < 3:
        return jsonify({'error': "User is too short"}), HTTP_400_BAD_REQUEST

    if not username.isalnum() or " " in username:
        return jsonify({'error': "Username should be alphanumeric, also no spaces"}), HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({'error': "Email is not valid"}), HTTP_400_BAD_REQUEST

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error': "Email is taken"}), HTTP_409_CONFLICT

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error': "username is taken"}), HTTP_409_CONFLICT

    pwd_hash = generate_password_hash(password)

    user = User(username=username, password=pwd_hash, email=email, user_role=role)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': "User created",
        'user': {

            'username': username, "email": email, "user_role":role
        }

    }), HTTP_201_CREATED


@auth.post('/login')
@swag_from('../docs/auth/login.yaml')
def login():
    username = request.json.get('username', '')
    password = request.json.get('password', '')

    user = User.query.filter_by(username=username).first()

    if user:
        is_pass_correct = check_password_hash(user.password, password)

        if is_pass_correct:
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)

            return jsonify({
                'user': {
                    'refresh': refresh,
                    'access': access,
                    'username': user.username,
                    'email': user.email,
                    'role': user.user_role
                }

            }), HTTP_200_OK

    return jsonify({'error': 'Wrong credentials'}), HTTP_401_UNAUTHORIZED


@auth.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        'username': user.username,
        'email': user.email
    }), HTTP_200_OK


@auth.get('/token/refresh')
@jwt_required(refresh=True)
def refresh_users_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return jsonify({
        'access': access
    }), HTTP_200_OK



@auth.get('/all_users')
@jwt_required()
@role_allowed(['sadmin'])
def get_all_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'user_role': user.user_role,
            # Add other user attributes as needed
        }
        user_list.append(user_data)
    return jsonify({'users': user_list})



@auth.get("/user/<int:id>")
@jwt_required()
@role_allowed(['sadmin'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), HTTP_404_NOT_FOUND
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'user_role': user.user_role,
        'created_at': user.created_at,
        'updated_at': user.updated_at
    }), HTTP_200_OK



@auth.delete("/<int:id>")
@jwt_required()
@role_allowed(['sadmin'])
def delete_user(id):
    current_user = get_jwt_identity()

    user = User.query.filter_by(user_id=current_user, id=id).first()

    if not user:
        return jsonify({'message': 'Item not found'}), HTTP_404_NOT_FOUND

    db.session.delete(user)
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT


@auth.get("/role")
@jwt_required()
@role_allowed(['company'])
def role():
   current_user = get_jwt_identity()

   return jsonify({"me": "my world"})
