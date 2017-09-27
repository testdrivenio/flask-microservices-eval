# project/api/exercises/exercises.py


from sqlalchemy import exc
from flask import Blueprint, jsonify, request

from project import db
from project.api.utils import authenticate
from project.api.exercises.models import Exercise


exercises_blueprint = Blueprint('exercises', __name__)


@exercises_blueprint.route('/exercises', methods=['GET'])
def get_all_exercises():
    """Get all exercises"""
    exercises = Exercise.query.all()
    exercises_list = []
    for exercise in exercises:
        exercise_object = {
            'id': exercise.id,
            'exercise_body': exercise.exercise_body,
            'test_code': exercise.test_code,
            'test_code_solution': exercise.test_code_solution,
            'created_at': exercise.created_at,
        }
        exercises_list.append(exercise_object)
    response_object = {
        'status': 'success',
        'data': {
            'exercises': exercises_list
        }
    }
    return jsonify(response_object), 200


@exercises_blueprint.route('/exercises', methods=['POST'])
@authenticate
def add_exercise(resp):
    """Add exercise"""
    if not resp['admin']:
        response_object = {
            'status': 'error',
            'message': 'You do not have permission to do that.'
        }
        return jsonify(response_object), 401
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
    exercise_body = post_data.get('exercise_body')
    test_code = post_data.get('test_code')
    test_code_solution = post_data.get('test_code_solution')
    try:
        db.session.add(Exercise(
            exercise_body=exercise_body,
            test_code=test_code,
            test_code_solution=test_code_solution))
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'New exercise was added!'
        }
        return jsonify(response_object), 201
    except (exc.IntegrityError, ValueError) as e:
        db.session().rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
