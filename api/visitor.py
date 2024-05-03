from os import access
from constants.http_status_codes import (HTTP_200_OK, HTTP_201_CREATED, 
                                         HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, 
                                         HTTP_409_CONFLICT, HTTP_404_NOT_FOUND, 
                                         HTTP_204_NO_CONTENT, HTTP_500_INTERNAL_SERVER_ERROR)

from flask import Blueprint, app, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from model.models import Visitor_card, Visitor, Employee, db
from utilites.checks import  role_allowed

visitor= Blueprint("visitor", __name__, url_prefix="/api/v1/visitor")



# Register Visitor API
@visitor.post('/register')
@jwt_required()
@role_allowed(['sadmin', 'company', 'staff', 'user'])
def register_visitor():
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

        # Query company ID associated with the user
        employee = Employee.query.filter_by(id=user_id).first()
        if employee:
            com_id = employee.com_id
        else:
            com_id = user_id
            
        # Create a new Visitor object
        new_visitor = Visitor(
            com_id=com_id,
            full_name=full_name,
            address=address,
            contact_details=contact_details,
            purpose_of_visit=purpose_of_visit,
            time_in=time_in,
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
def update_visitor(visitor_id):
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
@visitor.post('/register_card')
@jwt_required()
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

