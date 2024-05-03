from os import access
from constants.http_status_codes import (HTTP_200_OK, HTTP_201_CREATED, 
                                         HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, 
                                         HTTP_409_CONFLICT, HTTP_404_NOT_FOUND)
from flask import Blueprint, app, request, jsonify
from werkzeug.security import  generate_password_hash
import validators
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
from model.models import User, com_user, db
from utilites.checks import  role_allowed
from werkzeug.utils import secure_filename
import os


user1 = Blueprint("user1", __name__, url_prefix="/api/v1/user")


@user1.post('/register/<int:comp_id>')
@jwt_required()
@role_allowed(['sadmin'])
def register_by_id(comp_id):
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

    current_user_id = get_jwt_identity()  # Get the id of the current user
    new_user = com_user(
        user_id = current_user_id,
        com_id = comp_id,
        full_name = full_name,
        work_role = work_role
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'message': "local user created",
        'user': {

            'username': username, "email": email, "user_role":role, 'password': password
        },

        'Local User':{
            'full_name': full_name,
            'work_role': work_role
        }

    }), HTTP_201_CREATED



@user1.post('/register')
@jwt_required()
@role_allowed(['company'])
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

    current_user_id = get_jwt_identity()  # Get the id of the current user
    new_user = com_user(
        user_id = user.id,
        com_id = current_user_id,
        full_name = full_name,
        work_role = work_role
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'message': "local user created",
        'user': {

            'username': username, "email": email, "user_role":role, 'password': password
        },

        'Local User':{
            'full_name': full_name,
            'work_role': work_role
        }

    }), HTTP_201_CREATED




@user1.delete('/delete_samin/<int:user_id>')
@jwt_required()
@role_allowed(['sadmin', 'user1'])
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
    

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@user1.put('/update_image/<int:u_id>')
@jwt_required()
@role_allowed(['user1'])
def update_user_image(u_id):
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}),  HTTP_400_BAD_REQUEST

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}),  HTTP_400_BAD_REQUEST

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Generate a unique filename based on user_id
            unique_filename = f"user_{u_id}_{filename}"
            filepath = os.path.join('uploads', 'user1', u_id, unique_filename)
            file.save(filepath)

            user1 = com_user.query.get(u_id)
            if user1:
                user1.image = filepath
                db.session.commit()
                return jsonify({'message': 'User image updated successfully'}), HTTP_200_OK
            else:
                return jsonify({'error': 'User not found'}), HTTP_404_NOT_FOUND
        else:
            return jsonify({'error': 'File type not allowed'}), HTTP_400_BAD_REQUEST,
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR





# API endpoint to get user image by ID
@user1.get('/get_com_image/<int:u_id>')
@jwt_required()
def get_user1_logo(u_id):
    try:
        # Query the database to get the user by ID
        user1 = user1.query.get(u_id)
        if user1:
            # Check if the user has an image
            if user1.image:
                # Return the image file path
                return jsonify({'image_path': user1.image}), HTTP_200_OK
            else:
                return jsonify({'message': 'User does not have an image'}), HTTP_404_NOT_FOUND
        else:
            return jsonify({'error': 'User not found'}), HTTP_404_NOT_FOUND
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
