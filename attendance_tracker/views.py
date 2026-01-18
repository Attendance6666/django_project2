from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Student, Group, Attendance
import json
from datetime import datetime

# HTML Views
from django.http import HttpResponse

def home(request):
    """Main dashboard - TEMPORARY TEST"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Attendance Tracker - TEST</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 50px;
                text-align: center;
            }
            h1 { font-size: 3em; }
            .box {
                background: white;
                color: #333;
                padding: 30px;
                border-radius: 15px;
                margin: 20px auto;
                max-width: 600px;
            }
        </style>
    </head>
    <body>
        <h1>🎉 Django работает!</h1>
        <div class="box">
            <h2>Attendance Tracker System</h2>
            <p><strong>API работает:</strong></p>
            <p>✅ GET /api/students/</p>
            <p>✅ GET /api/attendance/</p>
            <p>✅ POST /api/attendance/</p>
            <br>
            <p><a href="/api/students/" style="color: #667eea; font-weight: bold;">Посмотреть студентов (JSON)</a></p>
            <p><a href="/admin/" style="color: #667eea; font-weight: bold;">Админ панель</a></p>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

def group_detail(request, group_id):
    """Detail view for a specific group showing all students"""
    group = get_object_or_404(Group, id=group_id)
    students = group.students.all().prefetch_related('attendance_set')
    
    context = {
        'group': group,
        'students': students,
    }
    return render(request, 'detail.html', context)

def students_list(request):
    """List all students (redirects to home for now)"""
    from django.shortcuts import redirect
    return redirect('home')


# API Views
@require_http_methods(["GET"])
def api_students_list(request):
    """
    GET /api/students/ - Get all students
    """
    students = Student.objects.select_related('group').all()
    
    students_data = []
    for student in students:
        students_data.append({
            'id': student.id,
            'first_name': student.first_name,
            'last_name': student.last_name,
            'student_id': student.student_id,
            'group': {
                'id': student.group.id,
                'name': student.group.name
            }
        })
    
    return JsonResponse({
        'status': 'success',
        'count': len(students_data),
        'data': students_data
    })

@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_attendance(request):
    """
    GET /api/attendance/ - Get all attendance records
    POST /api/attendance/ - Create new attendance record
    """
    if request.method == 'GET':
        # Get attendance records with optional filters
        attendance_records = Attendance.objects.select_related('student').all()
        
        # Optional: filter by date if provided in query params
        date_param = request.GET.get('date')
        if date_param:
            attendance_records = attendance_records.filter(date=date_param)
        
        data = []
        for record in attendance_records:
            data.append({
                'id': record.id,
                'student': {
                    'id': record.student.id,
                    'name': f"{record.student.first_name} {record.student.last_name}",
                    'student_id': record.student.student_id
                },
                'date': record.date.strftime('%Y-%m-%d'),
                'status': record.status
            })
        
        return JsonResponse({
            'status': 'success',
            'count': len(data),
            'data': data
        })
    
    elif request.method == 'POST':
        try:
            # Parse JSON body
            body = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['student_id', 'date', 'status']
            for field in required_fields:
                if field not in body:
                    return JsonResponse({
                        'status': 'error',
                        'message': f'Missing required field: {field}'
                    }, status=400)
            
            # Get student
            try:
                student = Student.objects.get(id=body['student_id'])
            except Student.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Student not found'
                }, status=404)
            
            # Validate status
            valid_statuses = ['present', 'absent', 'late']
            if body['status'] not in valid_statuses:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'
                }, status=400)
            
            # Parse date
            try:
                date_obj = datetime.strptime(body['date'], '%Y-%m-%d').date()
            except ValueError:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid date format. Use YYYY-MM-DD'
                }, status=400)
            
            # Create or update attendance
            attendance, created = Attendance.objects.update_or_create(
                student=student,
                date=date_obj,
                defaults={'status': body['status']}
            )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Attendance record created' if created else 'Attendance record updated',
                'data': {
                    'id': attendance.id,
                    'student': {
                        'id': student.id,
                        'name': f"{student.first_name} {student.last_name}"
                    },
                    'date': attendance.date.strftime('%Y-%m-%d'),
                    'status': attendance.status
                }
            }, status=201 if created else 200)
            
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)