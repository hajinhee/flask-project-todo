from app.db import todo_queries
from datetime import datetime


def get_all_todos():
    """모든 할 일 목록을 가져오는 함수"""
    todos = todo_queries.select_all_todos()
    return todos


def get_todo_by_id(todo_id):
    """특정 할 일을 ID로 조회하는 함수"""
    todo = todo_queries.select_todo_by_id(todo_id)
    
    # 예외 발생 시
    if not todo:
        raise Exception("Todo not found")
    return todo


def create_todo(no, content, reg_date, perform_date, is_completed):
    """새로운 할 일을 추가하는 함수"""
    
    todo_id = todo_queries.insert_todo(no, content, reg_date, perform_date, is_completed)
    
    if not todo_id:
        raise Exception("Todo not found")
    return todo_id


def update_todo(todo_id, user_code, task, perform_date, is_completed):
    """할 일을 업데이트하는 함수"""
    query = todo_queries.update_todo()
    return {"message": "Todo updated successfully!"}


def delete_todo(todo_id):
    """할 일을 삭제하는 함수"""
    query = todo_queries.delete_todo()
    return {"message": "Todo deleted successfully!"}
