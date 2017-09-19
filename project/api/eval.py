# project/api/eval.py


from flask import Blueprint, jsonify

from project.api.utils import authenticate


eval_blueprint = Blueprint('eval', __name__)


@eval_blueprint.route('/ping', methods=['GET'])
@authenticate
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })
