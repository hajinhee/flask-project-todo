from app.db.connection import engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

def select_all_todos():
    """모든 할 일 목록을 반환하는 쿼리"""
    
    query = """
    SELECT 
        id, 
        user_code, 
        no, 
        content, 
        is_completed, 
        DATE_FORMAT(reg_date, '%Y-%m-%d %H:%i:%S') AS reg_date, 
        DATE_FORMAT(update_date, '%Y-%m-%d %H:%i:%S') AS update_date, 
        DATE_FORMAT(perform_date, '%Y-%m-%d %H:%i:%S') AS perform_date
    FROM todo;
    """
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query))
            todos = result.mappings().fetchall()
            todos_dict = [dict(todo) for todo in todos]
            return todos_dict
    except Exception as e:
        print(f"Database error: {str(e)}")
        raise Exception(f"Database error: {str(e)}")


def select_todo_by_id(no):
    """특정 할 일을 ID로 조회하는 쿼리"""
    
    query = """
    SELECT 
        id, 
        user_code, 
        no, 
        content, 
        is_completed, 
        DATE_FORMAT(reg_date, '%Y-%m-%d %H:%i:%S') AS reg_date, 
        DATE_FORMAT(update_date, '%Y-%m-%d %H:%i:%S') AS update_date, 
        DATE_FORMAT(perform_date, '%Y-%m-%d %H:%i:%S') AS perform_date
    FROM todo WHERE no = :no;
    """
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query), {"no": no})
            todo = result.mappings().first()
            return dict(todo) if todo else None
    except Exception as e:
        print(f"Database error: {str(e)}")
        raise Exception(f"Database error: {str(e)}")


def insert_todo(no, content, reg_date, perform_date, is_completed):
    """새로운 할 일을 추가하는 쿼리"""
    
    query = """
        INSERT INTO todo (no, content, reg_date, perform_date, is_completed)
        VALUES (%s, %s, %s, %s, %s);
    """
    
    try:
        with engine.connect() as conn:
            conn.execute(query, (
                no,
                content,
                reg_date,
                perform_date,
                is_completed
            ))
            
            result = conn.execute("SELECT LAST_INSERT_ID()").fetchone()
            return dict(result)
    except Exception as e:
        print(f"Database error: {str(e)}")
        raise Exception(f"Database error: {str(e)}")


def update_todo(no, content, perform_date, update_date):
    """할 일을 업데이트하는 쿼리"""
    
    query = """
    UPDATE todo
    SET content = :content,
        perform_date = :perform_date,
        update_date = :update_date
    WHERE no = :no;
    """
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query), {
                "content": content,
                "no": no,
                "perform_date": perform_date,
                "update_date": update_date
            })
            conn.commit()
            if result.rowcount == 0:
                raise ValueError(f"Todo with No {no} not found for update.")
            return {"message": "Todo updated successfully!"}
    except Exception as e:
        print(f"Database error: {str(e)}")
        raise Exception(f"Database error: {str(e)}")


def delete_todo(todo_no):
    """할 일을 삭제하는 쿼리"""
    
    query = """
    DELETE FROM todo WHERE no = :todo_no;
    """
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query), {"todo_no": todo_no})
            
            if result.rowcount == 0:
                raise ValueError(f"Todo with ID {todo_no} not found for deletion.")
            return {"message": "Todo deleted successfully!"}
    except Exception as e:
        print(f"Database error: {str(e)}")
        raise Exception(f"Database error: {str(e)}")
