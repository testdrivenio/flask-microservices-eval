# project/api/eval.py


import io
import uuid

from flask import Blueprint, jsonify, request

from project.api.utils import authenticate
from project.api.docker_service import create_container, get_output


eval_blueprint = Blueprint('eval', __name__)


@eval_blueprint.route('/ping', methods=['GET'])
@authenticate
def ping_pong(resp):
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })
