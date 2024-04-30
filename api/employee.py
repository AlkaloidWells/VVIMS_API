from os import access
from constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT, HTTP_404_NOT_FOUND
from flask import Blueprint, app, request, jsonify
from werkzeug.security import generate_password_hash
import validators
from flask_jwt_extended import jwt_required, get_jwt_identity
from model.models import User, Employee, db
from utilites.checks import  role_not_allowed

employee = Blueprint("employee", __name__, url_prefix="/api/v1/employee")



@employee.post('/register')
@jwt_required()
@role_not_allowed(['staff'])
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
        com_id=current_user_id,  # Associate the employee with the current user's company
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
            'company_id': new_employee.com_id
        }
    }), HTTP_201_CREATED


@employee.get('/all_emp')
@jwt_required()
@role_not_allowed(['staff', "company"])
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
@role_not_allowed(['staff'])
def get_my_employees():
    current_user_id = get_jwt_identity()
    employees = Employee.query.filter_by(com_id=current_user_id).all()
    if not employees:
        return jsonify({'message': 'No employees found for this company'}), HTTP_404_NOT_FOUND
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
@role_not_allowed(['staff'])
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



@employee.delete('/delete_comp/<int:vircul_id>')
def delete_vircul(vircul_id):
    employee = Employee.query.get(vircul_id)
    if employee:
        db.session.delete(employee)
        db.session.commit()
        return jsonify({'message': 'Employee deleted successfully'}), HTTP_200_OK
    else:
        return jsonify({'message': 'Employee not found'}), HTTP_404_NOT_FOUND