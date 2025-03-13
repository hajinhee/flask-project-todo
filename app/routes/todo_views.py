from flask import Blueprint, request, jsonify
from app.db import todo_queries
from werkzeug.exceptions import BadRequest, NotFound
from datetime import datetime

todo_bp = Blueprint('todo', __name__, url_prefix='/todos')


def handle_exception(e):
    """예외 처리 및 서버 로그를 찍는 함수"""
    if isinstance(e, NotFound):
        print(f"Not Found: {str(e)}") 
        return jsonify({"error": str(e)}), 404
    elif isinstance(e, BadRequest):
        print(f"Bad Request: {str(e)}")
        return jsonify({"error": str(e)}), 400
    else:
        print(f"Internal Server Error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500
    
@todo_bp.route('/', methods=['GET'])
def get_todos():
    """모든 할 일 목록을 반환"""
    try:
        todos = todo_queries.select_all_todos()
        if not todos:
            raise NotFound("No todos found")
        return jsonify(todos), 200
    except Exception as e:
        return handle_exception(e)

@todo_bp.route('/<int:todo_no>', methods=['GET'])
def get_todo(todo_no):
    """특정 할 일을 조회하는 엔드포인트"""
    try:
        todo = todo_queries.select_todo_by_id(todo_no)
        if not todo:
            raise NotFound(f"Todo with No {todo_no} not found") 
        return jsonify(todo), 200
    except Exception as e:
        return handle_exception(e)


@todo_bp.route('/', methods=['POST'])
def add_todo():
    """새로운 할 일을 추가하는 엔드포인트"""
    try:
        todo_data = request.get_json()
        required_fields = ['no', 'content', 'regDate', 'performDate', 'checked']
        missing_fields = [field for field in required_fields if field not in todo_data]
        if missing_fields:
            raise BadRequest(f"Missing required fields: {', '.join(missing_fields)}")
        
        todo_id =todo_queries.insert_todo(**{
            "no": todo_data["no"],
            "content": todo_data["content"],
            "reg_date": todo_data["regDate"],
            "perform_date": todo_data["performDate"],
            "is_completed": todo_data["checked"]
        })
        if not todo_id:
            raise Exception("Failed to insert new todo")
        return jsonify(todo_id), 201
    except Exception as e:
        return handle_exception(e)


@todo_bp.route('/<int:todo_no>', methods=['PUT'])
def update_todo(todo_no):
    """기존 할 일을 수정하는 엔드포인트"""
    try:
        todo_data = request.get_json()
        
        content = todo_data.get('content')
        perform_date = todo_data.get('performDate')
        checked = todo_data.get('checked')
        
        if not any([content, perform_date, checked]):
            return jsonify({"error": "No fields to update"}), 400
        
        updated_fields = {}
        if content is not None:
            updated_fields['content'] = content
        if perform_date is not None:
            updated_fields['perform_date'] = perform_date
        if checked is not None:
            updated_fields['checked'] = checked
            
        update_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        rows_updated = todo_queries.update_todo(todo_no, content, perform_date, update_date)
        
        return jsonify(rows_updated), 204
    except Exception as e:
        return handle_exception(e)


@todo_bp.route('/<int:todo_no>', methods=['DELETE'])
def delete_todo(todo_no):
    """특정 할 일을 삭제하는 엔드포인트"""
    try:
        rows_deleted = todo_queries.delete_todo(todo_no)
        if rows_deleted == 0:
            raise NotFound(f"Todo with No {todo_no} not found for deletion")
        return jsonify(rows_deleted), 200
    except Exception as e:
        return handle_exception(e)