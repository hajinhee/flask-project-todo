from app.db.connection import engine
from sqlalchemy import text


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
        print(e)
        return e
 
 
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
        print(e)
        return e
    

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
        print(f"Error inserting todo: {e}")
        return None


def update_todo(todo_id, user_code, task, perform_date, is_completed):
    """할 일을 업데이트하는 쿼리"""
    
    query = """
    UPDATE todo
    SET user_code = :user_code,
        content = :task,
        perform_date = :perform_date,
        is_completed = :is_completed,
        update_date = :perform_date
    WHERE id = :todo_id;
    """
    
    try:
        with engine.connect() as conn:
            conn.execute(text(query), {
                "todo_id": todo_id,
                "user_code": user_code,
                "task": task,
                "perform_date": perform_date,
                "is_completed": is_completed
            })
            conn.commit()
    except Exception as e:
        print(e)
        return e


def delete_todo(todo_id):
    """할 일을 삭제하는 쿼리"""
    
    query = """
    DELETE FROM todo WHERE id = :todo_id;
    """
    
    try:
        with engine.connect() as conn:
            conn.execute(text(query), {"todo_id": todo_id})
            conn.commit()
    except Exception as e:
        print(e)
        return e
