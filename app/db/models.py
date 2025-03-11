# from sqlalchemy import Column, Integer, String, DateTime, Boolean

# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()


# class Todo(Base):
#     __tablename__ = 'todo'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     reg_date = Column(DateTime, nullable=False)
#     update_date = Column(DateTime, nullable=False)
#     user_code = Column(String(50), nullable=False)
#     no = Column(Integer, nullable=False)
#     perform_date = Column(DateTime, nullable=False)
#     content = Column(String(200), nullable=False)
#     is_completed = Column(Boolean, default=False)

#     def __repr__(self):
#         return f"<Todo(id={self.id}, content={self.content}, is_completed={self.is_completed})>"

#     def to_dict(self):
#         return {
#             "id": self.id,
#             "content": self.content,
#             "is_completed": self.is_completed,
#             "reg_date": self.reg_date.isoformat(),
#             "update_date": self.update_date.isoformat(),
#             "user_code": self.user_code,
#             "no": self.no,
#             "perform_date": self.perform_date.isoformat(),
#         }
