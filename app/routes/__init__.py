from .todo_views import todo_bp

def init_routes(app):
    """ 애플리케이션에 모든 라우트를 등록 """
    app.register_blueprint(todo_bp)  # todo_routes.py에서 정의한 블루프린트 등록