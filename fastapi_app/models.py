from sqlalchemy import Column, Integer, String, Date, ForeignKey
from fastapi_app.database import Base
from sqlalchemy import func
from sqlalchemy import DateTime

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer)
    course_id = Column(Integer)
    date = Column(Date)
    status = Column(String)

    
class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer)
    title = Column(String)
    description = Column(String)
    deadline = Column(Date)
    file_url = Column(String)
    created_by = Column(Integer)

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer)
    student_id = Column(Integer)
    file_url = Column(String)
    submitted_at = Column(DateTime, default=func.now())
    grade = Column(Integer, nullable=True)
    remarks = Column(String)

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    message = Column(String)
    link = Column(String, nullable=True)
    is_read = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())