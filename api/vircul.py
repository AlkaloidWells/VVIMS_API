from os import access
from constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT, HTTP_500_INTERNAL_SERVER_ERROR
from flask import Blueprint, app, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from model.models import Company, Vehicle, Employee, db
from utilites.checks import  role_not_allowed

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
            'message': 'Vehicle created successfully',
            'com_id': com_id,
            'plate_number': plate_number,
            'owner_details': owner_details,
            'model': model
        }), HTTP_201_CREATED
    except Exception as e:
        # Handle any exceptions here
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


# View Vehicule by ID
@vircul.get('/<int:vircul_id>')
def get_vircul_by_id(vircul_id):
    vircul = Vehicle.query.get(vircul_id)
    if vircul:
        return jsonify({
            'id': vircul.id,
            'com_id': vircul.com_id,
            'plate_number': vircul.plate_number,
            'make': vircul.make,
            'model': vircul.model,
            'color': vircul.color,
            'owner_details': vircul.owner_details,
            'entry_time': vircul.entry_time.isoformat(),
            'exit_time': vircul.exit_time.isoformat() if vircul.exit_time else None,
            'flagged_as_suspicious': vircul.flagged_as_suspicious,
            'created_at': vircul.created_at.isoformat(),
            'updated_at': vircul.updated_at.isoformat()
        }), HTTP_200_OK
    else:
        return jsonify({'message': 'Vehicule not found'}), HTTP_404_NOT_FOUND

# View All Vehicules
@vircul.get('/all_vec')
def get_all_virculs():
    virculs = Vehicle.query.all()
    vircul_list = []
    for vircul in virculs:
        vircul_data = {
            'id': vircul.id,
            'com_id': vircul.com_id,
            'plate_number': vircul.plate_number,
            'make': vircul.make,
            'model': vircul.model,
            'color': vircul.color,
            'owner_details': vircul.owner_details,
            'entry_time': vircul.entry_time.isoformat(),
            'exit_time': vircul.exit_time.isoformat() if vircul.exit_time else None,
            'flagged_as_suspicious': vircul.flagged_as_suspicious,
            'created_at': vircul.created_at.isoformat(),
            'updated_at': vircul.updated_at.isoformat()
        }
        vircul_list.append(vircul_data)
    return jsonify(vircul_list), HTTP_200_OK

# Delete Vehicule
@vircul.delete('/delete_vic/<int:vircul_id>')
def delete_vircul(vircul_id):
    vircul = Vehicle.query.get(vircul_id)
    if vircul:
        db.session.delete(vircul)
        db.session.commit()
        return jsonify({'message': 'Vehicule deleted successfully'}), HTTP_200_OK
    else:
        return jsonify({'message': 'Vehicule not found'}), HTTP_404_NOT_FOUND

# Update Vehicule
@vircul.put('/update_vec/<int:vircul_id>')
def update_vircul(vircul_id):
    vircul = Vehicle.query.get(vircul_id)
    if not vircul:
        return jsonify({'message': 'Vehicule not found'}), HTTP_404_NOT_FOUND

    data = request.get_json()
    vircul.plate_number = data.get('plate_number', vircul.plate_number)
    vircul.make = data.get('make', vircul.make)
    vircul.model = data.get('model', vircul.model)
    vircul.color = data.get('color', vircul.color)
    vircul.owner_details = data.get('owner_details', vircul.owner_details)
    vircul.entry_time = data.get('entry_time', vircul.entry_time)
    vircul.exit_time = data.get('exit_time', vircul.exit_time)
    vircul.flagged_as_suspicious = data.get('flagged_as_suspicious', vircul.flagged_as_suspicious)

    db.session.commit()
    return jsonify({'message': 'Vehicule updated successfully'}), HTTP_200_OK

# View Vehicules by Company using com_id
@vircul.get('/by_company/<int:com_id>')
def get_virculs_by_company(com_id):
    virculs = Vehicle.query.filter_by(com_id=com_id).all()
    if virculs:
        vircul_list = []
        for vircul in virculs:
            vircul_data = {
                'id': vircul.id,
                'com_id': vircul.com_id,
                'plate_number': vircul.plate_number,
                'make': vircul.make,
                'model': vircul.model,
                'color': vircul.color,
                'owner_details': vircul.owner_details,
                'entry_time': vircul.entry_time.isoformat(),
                'exit_time': vircul.exit_time.isoformat() if vircul.exit_time else None,
                'flagged_as_suspicious': vircul.flagged_as_suspicious,
                'created_at': vircul.created_at.isoformat(),
                'updated_at': vircul.updated_at.isoformat()
            }
            vircul_list.append(vircul_data)
        return jsonify(vircul_list), HTTP_200_OK
    else:
        return jsonify({'message': 'No Vehicules found for this company'}), HTTP_404_NOT_FOUND
