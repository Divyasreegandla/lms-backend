from django.http import JsonResponse
from django.db.models import Count, Avg
from .models import Attendance, Assignment, Submission

def dashboard(request):
    course_id = request.GET.get("course_id")
    if not course_id:
        return JsonResponse({
            "error":"course_id required"},status=400)

    
    total_students = Attendance.objects.filter(
        course_id=course_id
    ).values("student").distinct().count()

    avg_attendance = Attendance.objects.filter(
        course_id=course_id,
        status="Present"
    ).values("student").annotate(
        total=Count("id")
    ).aggregate(avg=Avg("total"))["avg"]


    total_assignments = Assignment.objects.filter(
        course_id=course_id
    ).count()

    submissions_count = Submission.objects.filter(
        assignment__course_id=course_id
    ).select_related("assignment").count()

    return JsonResponse({
        "total_students": total_students,
        "avg_attendance": avg_attendance or 0,
        "total_assignments": total_assignments,
        "submissions_count": submissions_count
    })