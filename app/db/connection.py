from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
from config import Config

# 엔진 생성
engine = create_engine(
    Config.DATABASE_URL,   
    encoding = 'utf-8',
    pool_size = 16,
    pool_recycle = 432,
    max_overflow = 32,
    pool_timeout = 86400,
    isolation_level = "AUTOCOMMIT"
)

# # 세션 클래스 생성
# Session = sessionmaker(bind=engine)

# def get_session():
#     return Session()
