from os import access
from constants.http_status_codes import (HTTP_200_OK, HTTP_201_CREATED, 
                                         HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, 
                                         HTTP_409_CONFLICT, HTTP_404_NOT_FOUND)
from flask import Blueprint, app, request, jsonify
from werkzeug.security import generate_password_hash
import validators
from flask_jwt_extended import jwt_required, get_jwt_identity
from model.models import User, Employee, db
from utilites.checks import  role_allowed
from werkzeug.utils import secure_filename
import os

employee = Blueprint("employee", __name__, url_prefix="/api/v1/employee")



@employee.post('/register')
@jwt_required()
@role_allowed(['company'])
def register():
    username = request.json['username']
    email = request.json['email']
    role = 'staff'
    password = request.json['password']
    
    full_name = request.json['full_name']
    staff_email = request.json['staff_email']
    staff_social_link = request.json['staff_social_link']
    staff_role = request.json['staff_role']
    staff_home_address = request.json['staff_home_address']
    staff_department = request.json['staff_department']
    image_path = request.json.get('image_path')  # Optional field

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

    current_user_id = get_jwt_identity()  # Get the id of the current user

    user = User(username=username, password=pwd_hash, email=email, user_role=role)
    db.session.add(user)
    db.session.commit()

    new_employee = Employee(
        user_id=user.id,
        com_id=current_user_id,  # Associate the employee with the current user's employee
        full_name=full_name,
        staff_email=staff_email,
        staff_social_link=staff_social_link,
        staff_role=staff_role,
        staff_home_address=staff_home_address,
        staff_department=staff_department,
        image_path=image_path
    )
    db.session.add(new_employee)
    db.session.commit()

    return jsonify({
        'message': "User created",
        'user': {
            'username': user.username,
            'email': user.email,
            'password': password  # or you can omit this for security reasons
        },
        'Employee': {
            'full_name': new_employee.full_name,
            'employee_id': new_employee.com_id
        }
    }), HTTP_201_CREATED



@employee.post('/register/<int:comp_id>')
@jwt_required()
@role_allowed(['sadmin'])
def register_by_id(comp_id):
    username = request.json['username']
    email = request.json['email']
    role = 'staff'
    password = request.json['password']
    
    full_name = request.json['full_name']
    staff_email = request.json['staff_email']
    staff_social_link = request.json['staff_social_link']
    staff_role = request.json['staff_role']
    staff_home_address = request.json['staff_home_address']
    staff_department = request.json['staff_department']
    image_path = request.json.get('image_path')  # Optional field

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

    new_employee = Employee(
        user_id=user.id,
        com_id=comp_id,  # Associate the employee with the current user's employee
        full_name=full_name,
        staff_email=staff_email,
        staff_social_link=staff_social_link,
        staff_role=staff_role,
        staff_home_address=staff_home_address,
        staff_department=staff_department,
        image_path=image_path
    )
    db.session.add(new_employee)
    db.session.commit()

    return jsonify({
        'message': "User created",
        'user': {
            'username': user.username,
            'email': user.email,
            'password': password  # or you can omit this for security reasons
        },
        'Employee': {
            'full_name': new_employee.full_name,
            'employee_id': new_employee.com_id
        }
    }), HTTP_201_CREATED





@employee.get('/all_emp')
@jwt_required()
@role_allowed(['sadmin'])
def get_all_employees():
    employees = Employee.query.all()
    employee_list = []
    for employee in employees:
        employee_data = {
            'id': employee.id,
            'full_name': employee.full_name,
            'staff_email': employee.staff_email,
            'staff_social_link': employee.staff_social_link,
            'staff_role': employee.staff_role,
            'staff_home_address': employee.staff_home_address,
            'staff_department': employee.staff_department,
            'image_path': employee.image_path,
            # Add other employee attributes as needed
        }
        employee_list.append(employee_data)
    return jsonify({'employees': employee_list})



@employee.get('/me')
@jwt_required()
@role_allowed(['company'])
def get_my_employee():
    current_user_id = get_jwt_identity()
    employee = Employee.query.filter_by(user_id=current_user_id).first()
    if not employee:
        return jsonify({'error': 'Employee not found'}), HTTP_404_NOT_FOUND
    employee_data = {
        'full_name': employee.full_name,
        'staff_email': employee.staff_email,
        'staff_social_link': employee.staff_social_link,
        'staff_role': employee.staff_role,
        'staff_home_address': employee.staff_home_address,
        'staff_department': employee.staff_department,
        'image_path': employee.image_path,
        # Add other employee attributes as needed
    }
    return jsonify(employee_data), HTTP_200_OK



@employee.get('/com_employees')
@jwt_required()
@role_allowed(['sadmin', 'company'])
def get_my_employees():
    current_user_id = get_jwt_identity()
    employees = Employee.query.filter_by(com_id=current_user_id).all()
    if not employees:
        return jsonify({'message': 'No employees found for this employee'}), HTTP_404_NOT_FOUND
    employees_data = []
    for employee in employees:
        employee_info = {
            'id': employee.id,
            'user_id': employee.user_id,
            'com_id': employee.com_id,
            'full_name': employee.full_name,
            'staff_email': employee.staff_email,
            'staff_social_link': employee.staff_social_link,
            'staff_role': employee.staff_role,
            'staff_home_address': employee.staff_home_address,
            'staff_department': employee.staff_department,
            'image_path': employee.image_path,
            'created_at': employee.created_at.isoformat(),
            'updated_at': employee.updated_at.isoformat()
            # Include other fields as needed
        }
        employees_data.append(employee_info)
    return jsonify(employees_data), HTTP_200_OK



@employee.get("/employee/<int:id>")
@jwt_required()
@role_allowed(['sadmin', 'company'])
def get_employee(id):
    employee = Employee.query.get(id)
    if not employee:
        return jsonify({'error': 'Employee not found'}), HTTP_404_NOT_FOUND
    return jsonify({
        'id': employee.id,
        'full_name': employee.full_name,
        'staff_email': employee.staff_email,
        'staff_social_link': employee.staff_social_link,
        'staff_role': employee.staff_role,
        'staff_home_address': employee.staff_home_address,
        'staff_department': employee.staff_department,
        'image_path': employee.image_path
    }), HTTP_200_OK



@employee.delete('/delete_emp/<int:emp_id>')
@jwt_required()
@role_allowed(['sadmin', 'company'])
def delete_emp(emp_id):
    employee = Employee.query.get(emp_id)
    if employee:
        user_id = employee.user_id
        db.session.delete(employee)
        db.session.commit()

        user = User.query.filter_by(id=user_id).first() 

        if not user:
            return jsonify({'message': 'User Item  not found'}), HTTP_404_NOT_FOUND

        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'Employee deleted successfully'}), HTTP_200_OK
    else:
        return jsonify({'message': 'Employee not found'}), HTTP_404_NOT_FOUND
    


@employee.put('/edit_emp/<int:emp_id>')
@employee.patch('/edit_emp/<int:emp_id>')
@jwt_required()
@role_allowed(['sadmin', 'company', 'satff'])
def editbookmark(com_id):
    
    employee = Employee.query.filter_by(id=com_id).first()

    if not employee:
        return jsonify({'message': 'Item not found'}), HTTP_404_NOT_FOUND

    full_name = request.json['full_name']
    staff_email = request.json['staff_email']
    staff_social_link = request.json['staff_social_link']
    staff_role = request.json['staff_role']
    staff_home_address = request.json['staff_home_address']
    staff_department = request.json['staff_department']
    


    employee.full_name = full_name
    employee.staff_email = staff_email
    employee.staff_department = staff_department
    employee.staff_social_links = staff_social_link
    employee.satf_role = staff_role
    employee.staff_home_adress = staff_home_address


    db.session.commit()

    return jsonify({
        'id': employee.id,
        'employee name': employee.full_name,
        'emp department': employee.staff_department,
    }), HTTP_200_OK




ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@employee.put('/update_image/<int:emp_id>')
@jwt_required()
@role_allowed(['staff'])
def update_user_image(emp_id):
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}),  HTTP_400_BAD_REQUEST

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}),  HTTP_400_BAD_REQUEST

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Generate a unique filename based on user_id
            unique_filename = f"user_{emp_id}_{filename}"
            filepath = os.path.join('uploads', 'employee', emp_id, unique_filename)
            file.save(filepath)

            employee = Employee.query.get(emp_id)
            if employee:
                employee.image = filepath
                db.session.commit()
                return jsonify({'message': 'User image updated successfully'}), HTTP_200_OK
            else:
                return jsonify({'error': 'User not found'}), HTTP_404_NOT_FOUND
        else:
            return jsonify({'error': 'File type not allowed'}), HTTP_400_BAD_REQUEST,
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR




# API endpoint to get user image by ID
@employee.get('/get_com_image/<int:emp_id>')
@jwt_required()
def get_emp_proc(emp_id):
    try:
        # Query the database to get the user by ID
        employee = Employee.query.get(emp_id)
        if employee:
            # Check if the user has an image
            if employee.image:
                # Return the image file path
                return jsonify({'image_path': employee.image}), HTTP_200_OK
            else:
                return jsonify({'message': 'User does not have an image'}), HTTP_404_NOT_FOUND
        else:
            return jsonify({'error': 'User not found'}), HTTP_404_NOT_FOUND
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
