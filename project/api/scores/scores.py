# project/api/scores/scores.py


from sqlalchemy import exc
from flask import Blueprint, jsonify, request

from project import db
from project.api.utils import authenticate
from project.api.scores.models import Score


scores_blueprint = Blueprint('scores', __name__)


@scores_blueprint.route('/scores', methods=['GET'])
def get_all_scores():
    """Get all scores"""
    scores = Score.query.all()
    scores_list = []
    for score in scores:
        score_object = {
            'id': score.id,
            'user_id': score.user_id,
            'exercise_id': score.exercise_id,
            'correct': score.correct,
            'created_at': score.created_at,
            'updated_at': score.updated_at,
        }
        scores_list.append(score_object)
    response_object = {
        'status': 'success',
        'data': {
            'scores': scores_list
        }
    }
    return jsonify(response_object), 200


@scores_blueprint.route('/scores/<score_id>', methods=['GET'])
def get_single_score(score_id):
    """Get single score"""
    response_object = {
        'status': 'fail',
        'message': 'Score does not exist'
    }
    try:
        score = Score.query.filter_by(id=int(score_id)).first()
        if not score:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'id': score.id,
                    'user_id': score.user_id,
                    'exercise_id': score.exercise_id,
                    'correct': score.correct,
                    'created_at': score.created_at,
                    'updated_at': score.updated_at
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@scores_blueprint.route('/scores/user', methods=['GET'])
@authenticate
def get_all_scores_by_user_id(resp):
    """Get all scores by user id"""
    scores = Score.query.filter_by(user_id=int(resp['data']['id'])).all()
    scores_list = []
    for score in scores:
        score_object = {
            'id': score.id,
            'user_id': score.user_id,
            'exercise_id': score.exercise_id,
            'correct': score.correct,
            'created_at': score.created_at,
            'updated_at': score.updated_at,
        }
        scores_list.append(score_object)
    response_object = {
        'status': 'success',
        'data': {
            'scores': scores_list
        }
    }
    return jsonify(response_object), 200


@scores_blueprint.route('/scores/user/<score_id>', methods=['GET'])
@authenticate
def get_single_score_by_user_id(resp, score_id):
    """Get single score by user id"""
    response_object = {
        'status': 'fail',
        'message': 'Score does not exist'
    }
    try:
        score = Score.query.filter_by(
            id=int(score_id),
            user_id=int(resp['data']['id'])
        ).first()
        if not score:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'id': score.id,
                    'user_id': score.user_id,
                    'exercise_id': score.exercise_id,
                    'correct': score.correct,
                    'created_at': score.created_at,
                    'updated_at': score.updated_at
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@scores_blueprint.route('/scores', methods=['POST'])
@authenticate
def add_score(resp):
    """Add score"""
    auth_user_id = int(resp['data']['id'])
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
    exercise_id = post_data.get('exercise_id')
    correct = post_data.get('correct')
    try:
        score = Score.query.filter_by(user_id=int(auth_user_id)).first()
        if not score:
            db.session.add(Score(
                user_id=auth_user_id,
                exercise_id=exercise_id,
                correct=correct))
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': 'New score was added!'
            }
            return jsonify(response_object), 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Sorry. That score already exists. Please update with a PUT request.'
            }
            return jsonify(response_object), 400
    except (exc.IntegrityError, ValueError) as e:
        db.session().rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400


@scores_blueprint.route('/scores/<score_id>', methods=['PUT'])
@authenticate
def update_score(resp, score_id):
    """Update score"""
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
    exercise_id = post_data.get('exercise_id')
    correct = post_data.get('correct')
    try:
        score = Score.query.filter_by(
            id=int(score_id),
            exercise_id=int(exercise_id),
            user_id=int(resp['data']['id'])
        ).first()
        if score:
            score.correct = correct
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': 'Score was updated!'
            }
            return jsonify(response_object), 200
        else:
            response_object = {
                'status': 'fail',
                'message': 'Sorry. That score does not exist.'
            }
            return jsonify(response_object), 400
    except (exc.IntegrityError, ValueError, TypeError) as e:
        db.session().rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400


@scores_blueprint.route('/scores', methods=['PATCH'])
@scores_blueprint.route('/scores/<score_id>', methods=['PATCH'])
@authenticate
def upsert_score(resp, score_id=None):
    """Upsert score"""
    auth_user_id = int(resp['data']['id'])
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
    exercise_id = post_data.get('exercise_id')
    correct = post_data.get('correct')
    try:
        filter_args = {
            'exercise_id': int(exercise_id),
            'user_id': int(resp['data']['id'])
        }
        if score_id:
            filter_args['id'] = int(score_id)

        score = Score.query.filter_by(**filter_args).first()
        if score:
            score.correct = correct
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': 'Score was updated!'
            }
            return jsonify(response_object), 200
        else:
            db.session.add(Score(
                user_id=auth_user_id,
                exercise_id=exercise_id,
                correct=correct))
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': 'New score was added!'
            }
            return jsonify(response_object), 201
    except (exc.IntegrityError, ValueError, TypeError) as e:
        db.session().rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
