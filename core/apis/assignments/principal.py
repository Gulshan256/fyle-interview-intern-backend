from flask import Blueprint
from flask import jsonify
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.models.teachers import Teacher
from core.models.assignments import AssignmentStateEnum, GradeEnum
from .schema import AssignmentSchema, AssignmentSubmitSchema,TeacherSchema,AssignmentGradeSchema

principal__assignments_resources = Blueprint('principal__assignments_resources', __name__)



@principal__assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    students_assignments = Assignment.get_submitted_and_graded_assignments()
    students_assignments_dump = AssignmentSchema().dump(students_assignments, many=True)
    return APIResponse.respond(data=students_assignments_dump)




@principal__assignments_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    """Returns list of teachers"""
    teachers = Teacher.get_all_teachers()
    teachers_dump = TeacherSchema().dump(teachers, many=True)
    return APIResponse.respond(data=teachers_dump)




@principal__assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

  
    if grade_assignment_payload.id is not None:
        assignment = Assignment.get_by_id(grade_assignment_payload.id)
        if assignment.state == AssignmentStateEnum.DRAFT:
            error_message = "Cannot grade assignments in Draft state"
            response = {
                "data": None,
                "message": error_message
            }
            return jsonify(response), 400  # Set the status code to 400 for an error response

    graded_assignment = Assignment.get_assignments_by_id_and_grade(grade_assignment_payload.id, grade_assignment_payload.grade)
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    # get response status code
    return APIResponse.respond(data=graded_assignment_dump)

