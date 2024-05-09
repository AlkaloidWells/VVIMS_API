from os import access
from constants.http_status_codes import (HTTP_200_OK, HTTP_201_CREATED, 
                                         HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, 
                                         HTTP_409_CONFLICT, HTTP_404_NOT_FOUND, 
                                         HTTP_204_NO_CONTENT, HTTP_500_INTERNAL_SERVER_ERROR)

from flask import Blueprint, app, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from model.models import Visitor_card, Visitor, Employee, Company, com_user, db
from utilites.checks import  role_allowed
from sqlalchemy import or_
from datetime import datetime

visitor= Blueprint("visitor", __name__, url_prefix="/api/v1/visitor")



# Register Visitor API
@visitor.post('/register/<int:comp_id>')
@jwt_required()
@role_allowed(['sadmin'])
def register_visitor_by_id(comp_id):
    try:
        data = request.get_json()
        full_name = data.get('full_name')
        address = data.get('address')
        contact_details = data.get('contact_details')
        purpose_of_visit = data.get('purpose_of_visit')
        time_in = data.get('time_in')
        badge_issued = data.get('badge_issued')

        # Get user ID from JWT token
        user_id = get_jwt_identity()
            
        # Create a new Visitor object
        time_in_datetime = datetime.strptime(time_in, "%Y-%m-%dT%H:%M:%S")
        new_visitor = Visitor(
            com_id=comp_id,
            full_name=full_name,
            address=address,
            contact_details=contact_details,
            purpose_of_visit=purpose_of_visit,
            time_in=time_in_datetime,
            badge_issued=badge_issued
        )

        db.session.add(new_visitor)
        db.session.commit()

        return jsonify({
            'message': 'Visitor created successfully',
            'visitor': {
                'id': new_visitor.id,
                'com_id': new_visitor.com_id,
                'full_name': new_visitor.full_name,
                'address': new_visitor.address,
                'contact_details': new_visitor.contact_details,
                'purpose_of_visit': new_visitor.purpose_of_visit,
                'time_in': new_visitor.time_in,
                'badge_issued': new_visitor.badge_issued
            }
        }),HTTP_201_CREATED
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR





@visitor.post('/register')
@jwt_required()
@role_allowed(['company','staff', 'user'])
def register_visitor():
    current_user_id = get_jwt_identity()

    company = Company.query.filter_by(user_id=current_user_id).first()
    employee = Employee.query.filter_by(user_id=current_user_id).first()
    user2 = com_user.query.filter_by(user_id=current_user_id).first()
  
    if company:
        com_id = company.id

    elif employee:
        com_id = employee.com_id
        
    elif user2:
        com_id = user2.com_id
            
    else:
        return jsonify({'error': 'Company not found'}), HTTP_404_NOT_FOUND
    
    try:
        data = request.get_json()
        full_name = data.get('full_name')
        address = data.get('address')
        contact_details = data.get('contact_details')
        purpose_of_visit = data.get('purpose_of_visit')
        time_in = data.get('time_in')
        badge_issued = data.get('badge_issued')

        time_in_datetime = datetime.strptime(time_in, "%Y-%m-%dT%H:%M:%S")
        new_visitor = Visitor(
            com_id=com_id,
            full_name=full_name,
            address=address,
            contact_details=contact_details,
            purpose_of_visit=purpose_of_visit,
            time_in=time_in_datetime,
            badge_issued=badge_issued
        )

        db.session.add(new_visitor)
        db.session.commit()

        return jsonify({
            'message': 'Visitor created successfully',
            'visitor': {
                'id': new_visitor.id,
                'com_id': new_visitor.com_id,
                'full_name': new_visitor.full_name,
                'address': new_visitor.address,
                'contact_details': new_visitor.contact_details,
                'purpose_of_visit': new_visitor.purpose_of_visit,
                'time_in': new_visitor.time_in,
                'badge_issued': new_visitor.badge_issued
            }
        }),HTTP_201_CREATED
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR




# Delete Visitor API
@visitor.delete("/delete/<int:visitor_id>")
@jwt_required()
@role_allowed(['sadmin', 'company', 'staff'])
def delete_visitor(visitor_id):
    try:
        current_user = get_jwt_identity()
        visitor = Visitor.query.filter_by(id=visitor_id, com_id=current_user).first()

        if not visitor:
            return jsonify({'message': 'Visitor not found'}), HTTP_404_NOT_FOUND

        db.session.delete(visitor)
        db.session.commit()

        return jsonify({'message': 'Visitor deleted successfully'}), HTTP_204_NO_CONTENT
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


# Update Visitor API
@visitor.put('/update/<int:visitor_id>')
@jwt_required()
@role_allowed(['sadmin', 'company', 'staff'])
def update_visitor_by_id(visitor_id):
    try:
        data = request.get_json()
        visitor = Visitor.query.filter_by(id=visitor_id).first()

        if not visitor:
            return jsonify({'error': 'Visitor not found'}), HTTP_404_NOT_FOUND

        # Update visitor data
        visitor.full_name = data.get('full_name', visitor.full_name)
        visitor.address = data.get('address', visitor.address)
        visitor.contact_details = data.get('contact_details', visitor.contact_details)
        visitor.purpose_of_visit = data.get('purpose_of_visit', visitor.purpose_of_visit)
        visitor.time_in = data.get('time_in', visitor.time_in)
        visitor.badge_issued = data.get('badge_issued', visitor.badge_issued)

        db.session.commit()

        return jsonify({'message': 'Visitor updated successfully', 'visitor': visitor}), HTTP_200_OK
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


# Update Visitor Card API
@visitor.put('/update_card/<int:visitor_id>')
@jwt_required()
@role_allowed(['sadmin', 'company', 'staff'])
def update_visitor_card(visitor_id):
    try:
        data = request.get_json()
        visitor_card = Visitor_card.query.get(visitor_id)

        if not visitor_card:
            return jsonify({'error': 'Visitor card not found'}), HTTP_404_NOT_FOUND

        # Update visitor card data
        visitor_card.surname = data.get('surname', visitor_card.surname)
        visitor_card.given_name = data.get('given_name', visitor_card.given_name)
        
        # Convert date string to Python date object
        dob_str = data.get('dob')
        if dob_str:
            visitor_card.dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
        
        visitor_card.pob = data.get('pob', visitor_card.pob)
        visitor_card.sex = data.get('sex', visitor_card.sex)
        visitor_card.proff = data.get('proff', visitor_card.proff)
        visitor_card.id_card_number = data.get('id_card_number', visitor_card.id_card_number)

        db.session.commit()

        # Return updated visitor card details
        updated_visitor_card = {
            'surname': visitor_card.surname,
            'given_name': visitor_card.given_name,
            'dob': visitor_card.dob.isoformat() if visitor_card.dob else None,
            'pob': visitor_card.pob,
            'sex': visitor_card.sex,
            'proff': visitor_card.proff,
            'id_card_number': visitor_card.id_card_number
        }

        return jsonify({'message': 'Visitor card updated successfully', 'visitor_card': updated_visitor_card}), HTTP_200_OK
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR




@visitor.post('/vic_search')
@jwt_required()
@role_allowed(['sadmin', 'company', 'staff', 'user'])
def search_visitors():
    try:
        search_criteria = request.json

        # Build the query dynamically based on the search criteria
        query = Visitor.query
        for key, value in search_criteria.items():
            # Check if the value is a substring (for case-insensitive search)
            query = query.filter(or_(Visitor.__dict__[key].ilike(f"%{value}%")))

        visitors = query.all()

        if not visitors:
            return jsonify({'message': 'No visitors found'}),HTTP_404_NOT_FOUND

        visitor_list = [{
            'id': visitor.id,
            'com_id': visitor.com_id,
            'full_name': visitor.full_name,
            'address': visitor.address,
            'contact_details': visitor.contact_details,
            'purpose_of_visit': visitor.purpose_of_visit,
            'time_in': visitor.time_in,
            'badge_issued': visitor.badge_issued,
            'created_at': visitor.created_at,
            'updated_at': visitor.updated_at
        } for visitor in visitors]

        return jsonify(visitor_list), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

@visitor.post('/search_card')
@jwt_required()
@role_allowed(['sadmin', 'company', 'staff', 'user'])
def search_visitor_cards():
    try:
        search_criteria = request.json

        # Build the query dynamically based on the search criteria
        query = Visitor_card.query
        for key, value in search_criteria.items():
            # Check if the value is a substring (for case-insensitive search)
            query = query.filter(or_(Visitor_card.__dict__[key].ilike(f"%{value}%")))

        visitor_cards = query.all()

        if not visitor_cards:
            return jsonify({'message': 'No visitor cards found'}), HTTP_404_NOT_FOUND

        visitor_card_list = [{
            'id': visitor_card.id,
            'com_id': visitor_card.com_id,
            'full_name': visitor_card.full_name,
            'address': visitor_card.address,
            'contact_details': visitor_card.contact_details,
            'purpose_of_visit': visitor_card.purpose_of_visit,
            'time_in': visitor_card.time_in,
            'badge_issued': visitor_card.badge_issued,
            'created_at': visitor_card.created_at,
            'updated_at': visitor_card.updated_at,
            'surname': visitor_card.surname,
            'given_name': visitor_card.given_name,
            'dob': visitor_card.dob if visitor_card.dob else None,
            'pob': visitor_card.pob,
            'sex': visitor_card.sex,
            'proff': visitor_card.proff,
            'id_card_number': visitor_card.id_card_number
        } for visitor_card in visitor_cards]

        return jsonify(visitor_card_list), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    




# View All Vehicules
@visitor.get('/all_vis')
@jwt_required()
@role_allowed(['sadmin'])
def get_all_visitors():
    visitor_card = Visitor_card.query.all()
    visitor_list = []
    for visitor in visitor_card:
        visitor_data = {
            'id': visitor.id,
            'com_id': visitor.com_id,
            'full_name': visitor.full_name,
            'address': visitor.address,
            'contact_details': visitor.contact_details,
            'purpose_of_visit': visitor.purpose_of_visit,
            'time_in': visitor.time_in,
            'badge_issued': visitor.badge_issued,
            'created_at': visitor.created_at,
            'updated_at': visitor.updated_at,
            'surname': visitor.surname,
            'given_name': visitor.given_name,
            'dob': visitor.dob,
            'pob': visitor.pob,
            'sex': visitor.sex,
            'proff': visitor.proff,
            'id_card_number': visitor.id_card_number
        }
        visitor_list.append(visitor_data)
    return jsonify(visitor_list), HTTP_200_OK



# View my visitors
@visitor.get('/my_visitors')
@jwt_required()
@role_allowed(['company', 'staff', 'user'])
def get_my_visitor():
    current_user_id = get_jwt_identity()

    company = Company.query.filter_by(user_id=current_user_id).first()
    employee = Employee.query.filter_by(user_id=current_user_id).first()
    user2 = com_user.query.filter_by(user_id=current_user_id).first()
  
    if company:
        com_id = company.id
    elif employee:
        com_id = employee.com_id
    elif user2:
        com_id = user2.com_id
    else:
        return jsonify({'error': 'Company not found'}), HTTP_404_NOT_FOUND

    visitor_cards = Visitor_card.query.filter_by(com_id=com_id).all()
    
    if visitor_cards:
        visitor_list = []
        for visitor in visitor_cards:
            visitor_data = {
                'id': visitor.id,
                'com_id': visitor.com_id,
                'full_name': visitor.full_name,
                'address': visitor.address,
                'contact_details': visitor.contact_details,
                'purpose_of_visit': visitor.purpose_of_visit,
                'time_in': visitor.time_in,
                'badge_issued': visitor.badge_issued,
                'created_at': visitor.created_at,
                'updated_at': visitor.updated_at,
                'surname': visitor.surname,
                'given_name': visitor.given_name,
                'dob': visitor.dob,
                'pob': visitor.pob,
                'sex': visitor.sex,
                'proff': visitor.proff,
                'id_card_number': visitor.id_card_number
            }
            visitor_list.append(visitor_data)
        return jsonify(visitor_list), HTTP_200_OK
    else:
        return jsonify({'message': 'No Visitors found for this company'}), HTTP_404_NOT_FOUND

    

#view visitors by company id
@visitor.get('/by_company/<int:com_id>')
@jwt_required()
@role_allowed(['sadmin'])
def get_visitor_by_company(com_id):
    visitor_card = Visitor_card.query.filter_by(com_id=com_id).all()
    if visitor:
        visitor_list = []
        for visitor in visitor_card:
            visitor_data = {
            'id': visitor.id,
            'com_id': visitor.com_id,
            'full_name': visitor.full_name,
            'address': visitor.address,
            'contact_details': visitor.contact_details,
            'purpose_of_visit': visitor.purpose_of_visit,
            'time_in': visitor.time_in,
            'badge_issued': visitor.badge_issued,
            'created_at': visitor.created_at,
            'updated_at': visitor.updated_at,
            'surname': visitor.surname,
            'given_name': visitor.given_name,
            'dob': visitor.dob,
            'pob': visitor.pob,
            'sex': visitor.sex,
            'proff': visitor.proff,
            'id_card_number': visitor.id_card_number
            }
            visitor_list.append(visitor_data)
        return jsonify(visitor_list), HTTP_200_OK
    else:
        return jsonify({'message': 'No Vehicules found for this company'}), HTTP_404_NOT_FOUND