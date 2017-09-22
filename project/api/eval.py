# project/api/eval.py


import io
import uuid

from flask import Blueprint, jsonify, request

from project.api.utils import authenticate
from project.api.docker_service import create_container, get_output


eval_blueprint = Blueprint('eval', __name__)


@eval_blueprint.route('/ping', methods=['GET'])
@authenticate
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@eval_blueprint.route('/eval', methods=['POST'])
@authenticate
def eval():
    # get post data
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'error',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
    data = post_data.get('code')
    if not data:
        response_object = {
            'status': 'error',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
    code = io.StringIO(data)
    # execute the code
    try:
        container_name = uuid.uuid4().hex
        create_container(code, container_name)
        output = get_output(container_name)
        return jsonify({
            'status': 'success',
            'output': output.decode('utf-8').rstrip()
        })
    except:
        response_object = {
            'status': 'error',
            'message': 'Something bad happened. Please try again.'
        }
        return jsonify(response_object), 500
