from os import access
from constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT, HTTP_404_NOT_FOUND
from flask import Blueprint, app, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import validators
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
from model.models import User, Company, db
from utilites.checks import  role_not_allowed

company = Blueprint("company", __name__, url_prefix="/api/v1/company")





@company.post('/register')
#@swag_from('./docs/auth/register.yaml')
@jwt_required()
@role_not_allowed(['staff', "company"])
def register():
    username = request.json['username']
    email = request.json['email']
    role = 'company'
    password = request.json['password']

    company_name = request.json['company_name']
    tax_number = request.json['tax_number']
    industry = request.json['industry']
    company_size = request.json['company_size']
    company_tel = request.json['company_tel']
    company_email = request.json['company_email']
    company_gps = request.json['company_gps']
    company_address = request.json['company_address']
    managed_by = request.json['managed_by']
    manager_role = request.json['manager_role']
    manager_tel = request.json['manager_tel']
    manager_email = request.json['manager_email']

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

    new_company = Company(
            user_id = user.id,
            company_name=company_name,
            tax_number=tax_number,
            industry=industry,
            company_size=company_size,
            company_tel=company_tel,
            company_email=company_email,
            company_gps=company_gps,
            company_address=company_address,
            managed_by=managed_by,
            manager_role=manager_role,
            manager_tel=manager_tel,
            manager_email=manager_email
    )
    db.session.add(new_company)
    db.session.commit()

    return jsonify({
    'message': "User created",
    'user': {
        'username': user.username,
        'email': user.email,
        'password': password  # or you can omit this for security reasons
    },
    'company': {
        'company_name': new_company.company_name,
        'tax_number': new_company.tax_number
    }

}), HTTP_201_CREATED

   

@company.get('/all_comp')
@jwt_required()
@role_not_allowed(['staff' 'company'])
def get_all_companies():
    companies = Company.query.all()
    company_list = []
    for company in companies:
        company_data = {
            'id': company.id,
            'company_name': company.company_name,
            'tax_number': company.tax_number,
            'industry': company.industry,
            'company_size': company.company_size,
            'company_tel': company.company_tel,
            'company_email': company.company_email,
            'company_gps': company.company_gps,
            'company_address': company.company_address,
            'managed_by': company.managed_by,
            'manager_role': company.manager_role,
            'manager_tel': company.manager_tel,
            'manager_email': company.manager_email,
            # Add other company attributes as needed
        }
        company_list.append(company_data)
    return jsonify({'companies': company_list})




@company.get('/me')
@jwt_required()
@role_not_allowed(['staff'])
def get_my_company():
    current_user_id = get_jwt_identity()
    company = Company.query.filter_by(user_id=current_user_id).first()
    if not company:
        return jsonify({'error': 'Company not found'}), HTTP_404_NOT_FOUND
    company_data = {
        'company_name': company.company_name,
        'tax_number': company.tax_number,
        'industry': company.industry,
        'company_size': company.company_size,
        'company_tel': company.company_tel,
        'company_email': company.company_email,
        'company_gps': company.company_gps,
        'company_address': company.company_address,
        'managed_by': company.managed_by,
        'manager_role': company.manager_role,
        'manager_tel': company.manager_tel,
        'manager_email': company.manager_email,
        # Add other company attributes as needed
    }
    return jsonify(company_data), HTTP_200_OK





@company.get("/company/<int:id>")
@jwt_required()
@role_not_allowed(['staff', 'company'])
def get_company(id):
    company = Company.query.get(id)
    if not company:
        return jsonify({'error': 'Company not found'}), HTTP_404_NOT_FOUND
    return jsonify({
        'id': company.id,
        'company_name': company.company_name,
        'tax_number': company.tax_number,
        'industry': company.industry,
        'company_size': company.company_size,
        'company_tel': company.company_tel,
        'company_email': company.company_email,
        'company_gps': company.company_gps,
        'company_address': company.company_address,
        'managed_by': company.managed_by,
        'manager_role': company.manager_role,
        'manager_tel': company.manager_tel,
        'manager_email': company.manager_email
    }), HTTP_200_OK


@company.delete('/delete_comp/<int:vircul_id>')
def delete_vircul(vircul_id):
    company = Company.query.get(vircul_id)
    if company:
        db.session.delete(company)
        db.session.commit()
        return jsonify({'message': 'Company deleted successfully'}), HTTP_200_OK
    else:
        return jsonify({'message': 'Companynot found'}), HTTP_404_NOT_FOUND