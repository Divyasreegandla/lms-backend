from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_app.database import SessionLocal, get_db
from fastapi_app.models import Attendance
from datetime import datetime
from fastapi import Query
from sqlalchemy import and_
from fastapi_app.notifications import create_notification

router = APIRouter()


@router.post("/attendance/mark")
def mark_attendance(payload: dict, db: Session = Depends(get_db)):
    try:
        date_obj = datetime.strptime(payload["date"], "%Y-%m-%d").date()

        for record in payload["records"]:
            exists = db.query(Attendance).filter_by(
                student_id=record["student_id"],
                course_id=payload["course_id"],
                date=date_obj
            ).first()

            if exists:
                raise HTTPException(status_code=400, detail="Duplicate attendance")

            attendance = Attendance(
                student_id=record["student_id"],
                course_id=payload["course_id"],
                date=date_obj,
                status=record["status"]
            )

            db.add(attendance)

        db.commit()
        for record in payload["records"]:
            create_notification(
                db,record["student_id"],"Attendance marked"
            )
        return {"message": "Attendance marked"}

    except Exception as e:
        return {"ERROR": str(e)}
    
@router.get("/attendance/student/{student_id}")
def get_student_attendance(
    student_id: int,
    course_id: int = Query(...),
    db: Session = Depends(get_db)
):
    records = db.query(Attendance).filter(
        Attendance.student_id == student_id,
        Attendance.course_id == course_id
    ).all()

    total = len(records)
    present = len([r for r in records if r.status == "Present"])

    percentage = (present / total * 100) if total > 0 else 0

    return {
        "total_classes": total,
        "present": present,
        "attendance_percentage": round(percentage, 2),
        "records": records
    }


@router.get("/attendance/course/{course_id}")
def get_course_attendance(
    course_id: int,
    from_date: str = Query(...),
    to_date: str = Query(...),
    db: Session = Depends(get_db)
):
    data = db.query(Attendance).filter(
        Attendance.course_id == course_id,
        Attendance.date.between(from_date, to_date)
    ).all()

    return {"records": data}

