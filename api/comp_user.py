from os import access
from constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT, HTTP_404_NOT_FOUND
from flask import Blueprint, app, request, jsonify
from werkzeug.security import  generate_password_hash
import validators
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
from model.models import User, com_user, db
from utilites.checks import  role_allowed

user1 = Blueprint("user1", __name__, url_prefix="/api/v1/user")


@user1.post('/register')
@jwt_required()
@role_allowed(['usn', 'company'])
def register():
    username = request.json['username']
    email = request.json['email']
    role = "user"
    password = request.json['password']


    full_name = request.json['full_name']
    work_role = request.json['work_role']
    

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

    new_user = com_user(
        user_id = user.id,
        full_name = full_name,
        work_role = work_role
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'message': "local user created",
        'user': {

            'username': username, "email": email, "user_role":role
        },

        'Local User':{
            'full_name': full_name,
            'work_role': work_role
        }

    }), HTTP_201_CREATED




@user1.delete('/delete_samin/<int:user_id>')
@jwt_required()
@role_allowed(['sadmin', 'company'])
def delete_usn(emp_id):
    us = com_user.query.get(emp_id)
    if us:
        user_id = us.user_id
        db.session.delete(us)
        db.session.commit()

        user = User.query.filter_by(id=user_id).first() 

        if not user:
            return jsonify({'message': 'User Item  not found'}), HTTP_404_NOT_FOUND

        db.session.delete(user)
        db.session.commit()
        
        return jsonify({'message': 'Local User deleted successfully'}), HTTP_200_OK
    else:
        return jsonify({'message': 'Local User not found'}), HTTP_404_NOT_FOUND