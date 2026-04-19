from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi_app.models import Assignment, Submission
from fastapi_app.database import get_db
from fastapi_app.notifications import create_notification
import os
import uuid

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/assignments/create")
async def create_assignment(
    title: str = Form(...),
    description: str = Form(...),
    deadline: str = Form(...),
    course_id: int = Form(...),
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    try:
        
        deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()
        
        file_url = None
        if file:
            
            file_extension = os.path.splitext(file.filename)[1]
            unique_filename = f"{uuid.uuid4().hex}{file_extension}"
            file_location = os.path.join(UPLOAD_DIR, unique_filename)
            
           
            with open(file_location, "wb") as f:
                content = await file.read()
                f.write(content)
            
            file_url = file_location
        
        assignment = Assignment(
            title=title,
            description=description,
            deadline=deadline_date,
            course_id=course_id,
            file_url=file_url,
            created_by=1 
        )
        
        db.add(assignment)
        db.commit()
        db.refresh(assignment)
        
       
        return {
            "message": "Assignment created successfully",
            "assignment_id": assignment.id,
            "title": assignment.title,
            "deadline": str(assignment.deadline),
            "file_url": file_url
        }
        
    except Exception as e:
        db.rollback()
        print(f"Error creating assignment: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create assignment: {str(e)}")

@router.post("/assignments/submit")
async def submit_assignment(
    assignment_id: int = Form(...),
    student_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
     
        assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
        if not assignment:
            raise HTTPException(status_code=404, detail="Assignment not found")
       
        if datetime.now().date() > assignment.deadline:
            raise HTTPException(status_code=400, detail="Deadline has passed")
      
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4().hex}{file_extension}"
        file_location = os.path.join(UPLOAD_DIR, unique_filename)
        
        with open(file_location, "wb") as f:
            content = await file.read()
            f.write(content)
   
        submission = Submission(
            assignment_id=assignment_id,
            student_id=student_id,
            file_url=file_location,
            submitted_at=datetime.now()
        )
        
        db.add(submission)
        db.commit()
        db.refresh(submission)
        
        # Create notification
        create_notification(db, student_id, f"Assignment '{assignment.title}' submitted successfully")
        
        return {
            "message": "Assignment submitted successfully",
            "submission_id": submission.id,
            "file_url": file_location,
            "submitted_at": submission.submitted_at
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        print(f"Error submitting assignment: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to submit: {str(e)}")

@router.get("/assignments/submissions")
def get_submissions(db: Session = Depends(get_db)):
    try:
        submissions = db.query(Submission).all()
        
        result = []
        for s in submissions:
           
            assignment = db.query(Assignment).filter(Assignment.id == s.assignment_id).first()
            
            result.append({
                "id": s.id,
                "assignment_id": s.assignment_id,
                "assignment_title": assignment.title if assignment else "Unknown",
                "student_id": s.student_id,
                "file_url": s.file_url,
                "submitted_at": s.submitted_at.isoformat() if s.submitted_at else None,
                "grade": s.grade,
                "remarks": s.remarks
            })
        
        return result
        
    except Exception as e:
        print(f"Error getting submissions: {str(e)}")
        return []

@router.get("/assignments/list")
def get_all_assignments(db: Session = Depends(get_db)):
    try:
        assignments = db.query(Assignment).all()
        
        result = []
        for a in assignments:
            result.append({
                "id": a.id,
                "title": a.title,
                "description": a.description,
                "deadline": str(a.deadline),
                "course_id": a.course_id,
                "file_url": a.file_url,
                "created_by": a.created_by
            })
        
        return result
        
    except Exception as e:
        print(f"Error getting assignments: {str(e)}")
        return []

@router.put("/assignments/grade")
def grade_submission(
    submission_id: int,
    grade: str,
    remarks: str = "",
    db: Session = Depends(get_db)
):
    try:
        submission = db.query(Submission).filter(Submission.id == submission_id).first()
        
        if not submission:
            raise HTTPException(status_code=404, detail="Submission not found")
        
        submission.grade = grade
        submission.remarks = remarks
        db.commit()
        
  
        assignment = db.query(Assignment).filter(Assignment.id == submission.assignment_id).first()
        
       
        create_notification(
            db, 
            submission.student_id, 
            f"Your submission for '{assignment.title if assignment else 'assignment'}' has been graded: {grade}"
        )
        
        return {"message": "Graded successfully", "grade": grade}
        
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        print(f"Error grading submission: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to grade: {str(e)}")