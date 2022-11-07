from urllib import response
from flask import Flask
from flask import jsonify, request
import requests
from flask_cors import CORS
from waitress import serve
import datetime
import re
import json

from flask_jwt_extended import create_access_token, verify_jwt_in_request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_jwt_extended import JWTManager

# ------------------------- Setting Flask App -------------------------------

app = Flask(__name__)
cors = CORS(app)

def loadFileConfig():
    with open('config.json') as f:
        data = json.load(f)
    return data

dataConfig = loadFileConfig()

app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)

headers = {"Content-Type": "application/json; charset=utf-8"}


# ------------------------- Middleware -------------------------------
@app.before_request
def before_request_callback():
    endPoint = clean_url(request.path)
    excludeRoutes = ['/login']
    if excludeRoutes.__contains__(request.path):
        print("ruta excluida",request.path)
        pass
    elif verify_jwt_in_request():
        user = get_jwt_identity()
        if user["rol"] is not None:
            havePermission = validate_permission(endPoint,request.method,user["rol"]["id"])
            if not havePermission:

                return jsonify({"message": "Permission denied"}),401
        else:
            return jsonify({"message": "Permission denied"}),401
