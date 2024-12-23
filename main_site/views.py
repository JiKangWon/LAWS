from django.shortcuts import render
from datetime import datetime
from django.http import JsonResponse
from .models import *

# Create your views here.
def get_home(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username, password=password).first()
        user_inf = UserInfo.objects.filter(user=user).first()
        if user:
            context = {
                'user':user,
                'user_inf': user_inf,  
            }
            return render(request, 'page/home.html', context)
    return render(request, 'log/login.html')

def get_todolist(request, id):
    user = User.objects.filter(id=id).first()
    user_inf = UserInfo.objects.filter(user=user).first()
    term = Term.objects.filter(user=user).first()
    context = {
        'user':user,
        'user_inf': user_inf,   
        'term':term,
        }
    return render(request, 'page/todolist.html', context)

def get_open_shift(request, id):
    # todo: Xử lý thông tin mở ca:
    if request.method == 'POST':
        shift = Shift.objects.create(
            name = request.POST.get('shiftName'),
        )
        for i in range(1,5):
            # todo: Lấy dữ liệu
            coursePost = request.POST.get(f'Course{i}')
            datePost = request.POST.get(f'Time{i}')
            # todo: Tạo mới session
            courseId = int(coursePost) if coursePost else None
            course = Course.objects.filter(id = courseId).first()
            subject = course.subject if course else None
            classObj = subject.class_object if subject else None
            date = datetime.fromisoformat(datePost) if datePost else None
            type = request.POST.get(f'Type{i}')
            session = Session.objects.create(
                shift = shift,
                date = date,
                type = type,
                class_obj = classObj,
                subject = subject,
                course = course,
            )
            chapter = Chapter.objects.filter(id = 3).first()
            session.chapter.add(chapter)  
    # todo: Đẩy dữ liệu của người dùng lên web
    user = User.objects.filter(id=id).first()
    user_inf = UserInfo.objects.filter(user=user).first()
    term = Term.objects.filter(user=user).first()
    classes = Class.objects.filter(term=term)
    context = {
        'user':user,
        'user_inf': user_inf,   
        'term':term,
        'classes':classes,
        }
    return render(request, 'page/open_shift.html', context)

def get_close_shift(request, id):
    user = User.objects.filter(id=id).first()
    user_inf = UserInfo.objects.filter(user=user).first()
    term = Term.objects.filter(user=user).first()
    classes = Class.objects.filter(term=term)
    context = {
        'user':user,
        'user_inf': user_inf,   
        'term':term,
        'classes':classes,
        }
    return render(request, 'page/close_shift.html', context)

def get_subject(request):
    class_id = request.GET.get('class_id')
    subjects = Subject.objects.filter(class_object_id=class_id)
    return JsonResponse({'subjects':list(subjects.values('id','name'))})

def get_course(request):
    subject_id = request.GET.get('subject_id')
    courses = Course.objects.filter(subject_id=subject_id)
    return JsonResponse({'courses':list(courses.values('id','name'))})
