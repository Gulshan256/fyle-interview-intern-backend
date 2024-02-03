from flask import Blueprint
from flask import jsonify
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, AssignmentGradeSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    teachers_assignments = Assignment.get_assignments_by_teacher(p.teacher_id)
    teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)
    return APIResponse.respond(data=teachers_assignments_dump)


@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    assignment=Assignment.get_by_id(grade_assignment_payload.id)
   
    if assignment is not None and  assignment.teacher_id != p.teacher_id:
        response = {
            "data": None,
            "error": "FyleError",
            "message": "assignment not submitted to this teacher"
        }
        return jsonify(response), 400
    
    # check for grade 
    if assignment is not None and assignment.grade != grade_assignment_payload.grade:
        response = {
            "error": "ValidationError"
        }
        return jsonify(response), 400

    # check for id 
    if assignment is None or assignment.id != grade_assignment_payload.id:
        response = {
            "error": "FyleError"
        }
        return jsonify(response), 404
    
    # only a submitted assignment can be graded
    if assignment is not None and assignment.state != "submitted":
        response = {
            "error": "FyleError"
        }
        return jsonify(response), 400

    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)
