from os import access
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT, HTTP_500_INTERNAL_SERVER_ERROR
from flask import Blueprint, app, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.model.models import Company, Vehicle, Employee, db
from utilites.checks import  role_required

vircul= Blueprint("vircul", __name__, url_prefix="/api/v1/vircul")


@vircul.post('/register')
@jwt_required()
def register():
    try:
        data = request.get_json()
        required_fields = ['plate_number', 'make', 'model', 'color', 'owner_details', 'entry_time']
        for field in required_fields:
            if field not in data:
                return {'error': f"Missing required field: {field}"}, HTTP_400_BAD_REQUEST,

        plate_number = data.get('plate_number')
        make = data.get('make')
        model = data.get('model')
        color = data.get('color')
        owner_details = data.get('owner_details')
        entry_time = data.get('entry_time')
        exit_time = data.get('exit_time')
        flagged_as_suspicious = data.get('flagged_as_suspicious', False)

        user_id = get_jwt_identity()

        cum2 = Employee.query.filter_by(id=user_id).first()
        if cum2:
            com_id = cum2.com_id
        else:
            com_id = user_id
            
        new_vehicle = Vehicle(
            com_no=com_id,
            plate_number=plate_number,
            make=make,
            model=model,
            color=color,
            owner_details=owner_details,
            entry_time=entry_time,
            exit_time=exit_time,
            flagged_as_suspicious=flagged_as_suspicious
        

        )

        db.session.add(new_vehicle)
        db.session.commit()

        return jsonify({
            'message': 'Vircule created successfully',
            'com_id': com_id,
            'plat_number': plate_number,
            'owner_details': owner_details,
            'model': model
        }), HTTP_201_CREATED
    except Exception as e:
        # Handle any exceptions here
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR