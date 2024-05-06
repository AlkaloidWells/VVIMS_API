from os import access
from constants.http_status_codes import (HTTP_200_OK, HTTP_201_CREATED, 
                                         HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR , 
                                         HTTP_409_CONFLICT, HTTP_404_NOT_FOUND
                                        )
from flask import Blueprint, app, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import validators
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
from model.models import User, Super_Admin, db
from utilites.checks import  role_allowed
from werkzeug.utils import secure_filename
import os
sadmin = Blueprint("sadmin", __name__, url_prefix="/api/v1/sadmin")


@sadmin.post('/register')
@jwt_required()
@role_allowed(['sadmin'])
def register():
    username = request.json['username']
    email = request.json['email']
    role = "sadmin"
    password = request.json['password']


    full_name = request.json['full_name']

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

    new_sadmin = Super_Admin(
        user_id = user.id,
        full_name = full_name
    )

    db.session.add(new_sadmin)
    db.session.commit()

    return jsonify({
        'message': "Super Admin created",
        'user': {

            'username': username, "email": email, "user_role":role
        },

        'super_admin':{
            'full_name': full_name
        }

    }), HTTP_201_CREATED




@sadmin.delete('/delete_samin/<int:sadmin_id>')
@jwt_required()
@role_allowed(['sadmin'])
def delete_sadmin(emp_id):
    sadmin = Super_Admin.query.get(emp_id)
    if sadmin:
        user_id = sadmin.user_id
        db.session.delete(sadmin)
        db.session.commit()

        user = User.query.filter_by(id=user_id).first() 

        if not user:
            return jsonify({'message': 'User Item  not found'}), HTTP_404_NOT_FOUND

        db.session.delete(user)
        db.session.commit()
        
        return jsonify({'message': 'Super_Admin deleted successfully'}), HTTP_200_OK
    else:
        return jsonify({'message': 'Super_Admin not found'}), HTTP_404_NOT_FOUND
    


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@sadmin.put('/update_image/<int:ad_id>')
@jwt_required()
@role_allowed(['sadmin'])
def update_user_image(ad_id):
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}),  HTTP_400_BAD_REQUEST

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}),  HTTP_400_BAD_REQUEST

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Generate a unique filename based on user_id
            unique_filename = f"user_{ad_id}_{filename}"
            filepath = os.path.join('uploads', 'sadmin', ad_id, unique_filename)
            file.save(filepath)

            sadmin = Super_Admin.query.get(ad_id)
            if sadmin:
                sadmin.image = filepath
                db.session.commit()
                return jsonify({'message': 'User image updated successfully'}), HTTP_200_OK
            else:
                return jsonify({'error': 'User not found'}), HTTP_404_NOT_FOUND
        else:
            return jsonify({'error': 'File type not allowed'}), HTTP_400_BAD_REQUEST,
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR




# API endpoint to get user image by ID
@sadmin.get('/get_com_image/<int:ad_id>')
@jwt_required()
def get_sadmin_logo(ad_id):
    try:
        # Query the database to get the user by ID
        sadmin = Super_Admin.query.get(ad_id)
        if sadmin:
            # Check if the user has an image
            if sadmin.image:
                # Return the image file path
                return jsonify({'image_path': sadmin.image}), HTTP_200_OK
            else:
                return jsonify({'message': 'User does not have an image'}), HTTP_404_NOT_FOUND
        else:
            return jsonify({'error': 'User not found'}), HTTP_404_NOT_FOUND
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
