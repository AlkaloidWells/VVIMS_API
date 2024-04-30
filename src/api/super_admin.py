from os import access
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT
from flask import Blueprint, app, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
# import validators
# from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
# from flasgger import swag_from
from src.model.models import User, Super_Admin

sadmin= Blueprint("sadmin", __name__, url_prefix="/api/v1/sadmin")

@sadmin.post('/register')
def reg_sadmin():
    return "User Registerd"
