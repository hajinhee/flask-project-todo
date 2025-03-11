from flask import Flask
from flask_cors import CORS
from .routes import init_routes


def create_app():
    app = Flask(__name__)
    
    # 환경 변수 설정
    app.config.from_object("config.Config")

    # CORS 설정 (React와 API를 연결)
    CORS(app)
    
    # 라우트 초기화
    init_routes(app)

    return app