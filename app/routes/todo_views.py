from flask import Blueprint, request, jsonify, Response, json
from app.services import todo_service
from werkzeug.exceptions import BadRequest, NotFound

todo_bp = Blueprint('todo', __name__, url_prefix='/todos')


@todo_bp.route('/', methods=['GET'])
def get_todos():
    """모든 할 일 목록을 반환"""

    todos = todo_service.get_all_todos()
    try: 
        return jsonify(todos), 200
    except ValueError as e:
        return str(e), 404
    
    
@todo_bp.route('/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    """모든 할 일 목록을 반환하는 엔드포인트"""
    try:
        todo = todo_service.get_todo_by_id(todo_id)
        
        if not todo:
            raise NotFound(f"Todo with ID {todo_id} not found")
        
        return jsonify(todo), 200
    
    except NotFound as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@todo_bp.route('/', methods=['POST'])
def add_todo():
    """새로운 할 일을 추가하는 엔드포인트"""
    
    try:
        todo_data = request.get_json()
        
        required_fields = ['id', 'content', 'regDate', 'performDate', 'checked']
        missing_fields = [field for field in required_fields if field not in todo_data]
        
        if missing_fields:
            raise BadRequest(f"Missing required fields: {', '.join(missing_fields)}")
        
        todo_id = todo_service.create_todo(**{
            "no": todo_data["id"],
            "content": todo_data["content"],
            "reg_date": todo_data["regDate"],
            "perform_date": todo_data["performDate"],
            "is_completed": todo_data["checked"]
        })
        
        if not todo_id:
            raise Exception("Failed to save data. Please try again later.")
        
        return jsonify({"id": todo_id}), 201
    
    except BadRequest as e:
        print(f"BadRequest 오류 발생: {e}")
        return jsonify({"error": str(e)}), 400
    
    except Exception as e:
        print(f"Exception 오류 발생: {e}")
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@todo_bp.route('/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """기존 할 일을 수정하는 엔드포인트"""
    try:
        todo_data = request.get_json()
        todo_service.update_todo(todo_id, todo_data)
        return '', 204
    except ValueError as e:
        return str(e), 404


@todo_bp.route('/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """특정 할 일을 삭제하는 엔드포인트"""
    try:
        todo_service.delete_todo(todo_id)
        return '', 204
    except ValueError as e:
        return str(e), 404
