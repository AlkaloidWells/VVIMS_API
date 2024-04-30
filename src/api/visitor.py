from os import access
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT, HTTP_500_INTERNAL_SERVER_ERROR
from flask import Blueprint, app, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.model.models import Company, Visitor, Employee, db
from src.utilites.checks import  role_not_allowed


visitor= Blueprint("visitor", __name__, url_prefix="/api/v1/visitor")

@visitor.post('/register')
@jwt_required()
def register():
    try:
        data = request.get_json()
        full_name = data.get('full_name')
        id_card_number = data.get('id_card_number')
        date_of_birth = data.get('date_of_birth')
        address = data.get('address')
        contact_details = data.get('contact_details')
        purpose_of_visit = data.get('purpose_of_visit')
        time_in = data.get('time_in')
        badge_issued = data.get('badge_issued')

        user_id = get_jwt_identity()

        cum2 = Employee.query.filter_by(id=user_id).first()
        if cum2:
            com_id = cum2.com_id
        else:
            com_id = user_id
            
        new_visitor = Visitor(
            com_id=com_id,
            full_name=full_name,
            id_card_number=id_card_number,
            date_of_birth=date_of_birth,
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
            'com_id': com_id,
            'full_name': full_name,
            'id_card_number': id_card_number,
            'date_of_birth': date_of_birth
        }), HTTP_201_CREATED
    except Exception as e:
        # Handle any exceptions here
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR



@visitor.delete("/delete_vis/<int:id>")
@jwt_required()
def delete_visitor(id):
    current_user = get_jwt_identity()

    visitor = Visitor.query.filter_by(user_id=current_user, id=id).first()

    if not visitor:
        return jsonify({'message': 'Item not found'}), HTTP_404_NOT_FOUND

    db.session.delete(visitor)
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT



# View all visitors
@visitor.get('/all_visitors')
@jwt_required()
def view_all_visitors():
    visitors = Visitor.query.all()
    visitor_list = [{
        'id': visitor.id,
        'com_id': visitor.com_id,
        'full_name': visitor.full_name,
        'id_card_number': visitor.id_card_number,
        'date_of_birth': visitor.date_of_birth,
        'address': visitor.address,
        'contact_details': visitor.contact_details,
        'purpose_of_visit': visitor.purpose_of_visit,
        'time_in': visitor.time_in.isoformat(),
        'badge_issued': visitor.badge_issued
    } for visitor in visitors]
    return jsonify(visitor_list)

# View visitor detail by ID
@visitor.get('/visitor/<int:visitor_id>')
def view_visitor_detail(visitor_id):
    visitor = Visitor.query.get(visitor_id)
    if not visitor:
        return jsonify({'error': 'Visitor not found'}), HTTP_404_NOT_FOUND
    return jsonify({
        'id': visitor.id,
        'com_id': visitor.com_id,
        'full_name': visitor.full_name,
        'id_card_number': visitor.id_card_number,
        'date_of_birth': visitor.date_of_birth,
        'address': visitor.address,
        'contact_details': visitor.contact_details,
        'purpose_of_visit': visitor.purpose_of_visit,
        'time_in': visitor.time_in.isoformat(),
        'badge_issued': visitor.badge_issued
    })

# View visitors by company ID
@visitor.get('/by_company/<int:company_id>')
def view_visitors_by_company(company_id):
    visitors = Visitor.query.filter_by(com_id=company_id).all()
    if not visitors:
        return jsonify({'message': 'No visitors found for this company'}), HTTP_404_NOT_FOUND
    visitor_list = [{
        'id': visitor.id,
        'com_id': visitor.com_id,
        'full_name': visitor.full_name,
        'id_card_number': visitor.id_card_number,
        'date_of_birth': visitor.date_of_birth,
        'address': visitor.address,
        'contact_details': visitor.contact_details,
        'purpose_of_visit': visitor.purpose_of_visit,
        'time_in': visitor.time_in.isoformat(),
        'badge_issued': visitor.badge_issued
    } for visitor in visitors]
    return jsonify(visitor_list), HTTP_200_OK



# Update Visitor
@visitor.put('update_vis/<int:visitor_id>')
def update_visitor(visitor_id):
    visitor = Visitor.query.get(visitor_id)
    if not visitor:
        return jsonify({'message': 'Visitor not found'}), HTTP_404_NOT_FOUND

    data = request.get_json()
    visitor.full_name = data.get('full_name', visitor.full_name)
    visitor.id_card_number = data.get('id_card_number', visitor.id_card_number)
    visitor.date_of_birth = data.get('date_of_birth', visitor.date_of_birth)
    visitor.address = data.get('address', visitor.address)
    visitor.contact_details = data.get('contact_details', visitor.contact_details)
    visitor.purpose_of_visit = data.get('purpose_of_visit', visitor.purpose_of_visit)
    visitor.time_in = data.get('time_in', visitor.time_in)
    visitor.badge_issued = data.get('badge_issued', visitor.badge_issued)

    db.session.commit()
    return jsonify({'message': 'Visitor updated successfully'}), HTTP_200_OK
