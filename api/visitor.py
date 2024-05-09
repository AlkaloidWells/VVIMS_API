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


# Register Visitor Card API
@visitor.post('/register_card/int:visitor_id>')
@jwt_required(id)
@role_allowed(['sadmin', 'company', 'staff'])
def register_visitor_card():
    try:
        data = request.json
        surname = data.get('surname')
        given_name = data.get('given_name')
        dob = data.get('dob')
        pob = data.get('pob')
        sex = data.get('sex')
        proff = data.get('proff')
        id_card_number = data.get('id_card_number')

        if not all([surname, given_name, dob, pob, sex, proff, id_card_number]):
            return jsonify({'error': 'Missing required fields'}), HTTP_400_BAD_REQUEST

        new_visitor_card = Visitor_card(surname=surname, 
                                        given_name=given_name,
                                        dob=dob, pob=pob, 
                                        sex=sex, 
                                        proff=proff, 
                                        id_card_number=id_card_number)
        
        db.session.add(new_visitor_card)
        db.session.commit()

        return jsonify({'message': 'Visitor card registered successfully', 'visitor_card': new_visitor_card}), HTTP_201_CREATED
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


# Update Visitor API
@visitor.put('/update_card/<int:visitor_id>')
@jwt_required()
@role_allowed(['sadmin', 'company', 'staff'])
def update_visitor_card(visitor_id):
    try:
        data = request.get_json()
        visitor = Visitor.query.get(visitor_id)

        if not visitor:
            return jsonify({'error': 'Visitor not found'}), HTTP_404_NOT_FOUND

        # Update visitor data
        visitor.full_name = data.get('full_name', visitor.full_name)
        visitor.date_of_birth = data.get('date_of_birth', visitor.date_of_birth)
        visitor.sex = data.get('sex', visitor.sex)
        visitor.id_card_number = data.get('id_card_number', visitor.id_card_number)

        db.session.commit()

        # Return updated visitor details
        updated_visitor = {
            'full_name': visitor.full_name,
            'date_of_birth': visitor.date_of_birth,
            'sex': visitor.sex,
            'id_card_number': visitor.id_card_number
        }

        return jsonify({'message': 'Visitor updated successfully', 'visitor': updated_visitor}), HTTP_200_OK
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
@role_allowed(['sadmin'])
def get_all_visitors():
    visitor_card = Visitor.query.all()
    visitor_list = []
    for visitor in visitor_card:
        visitor_data = {
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
        }
        visitor_list.append(visitor_data)
    return jsonify(visitor_list), HTTP_200_OK