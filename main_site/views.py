from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import datetime
from django.http import JsonResponse, HttpResponse
from .models import *
from django.utils.timezone import make_aware

# Create your views here.
def getHome(request):
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
    shift = Shift.objects.filter(endTime__gt=timezone.now(), user=user).first()
    sessions = Session.objects.filter(shift=shift)
    context = {
        'user':user,
        'user_inf': user_inf,   
        'term':term,
        'shift':shift,
        'sessions':sessions,
        }
    return render(request, 'page/todolist.html', context)

def getOpenShift(request, id):
    user = User.objects.filter(id=id).first()
    term = Term.objects.filter(user=user).first()
    classes = Class.objects.filter(term=term)
    numberRange = range(1,5)
    context = {
        'user':user,
        'numberRange':numberRange,
        'term':term,
        'classes':classes,
    }
    if request.method == 'POST':
        shiftName = request.POST.get('shiftName')
        shift = Shift.objects.create(
            name = shiftName,
            user = user,
        )
        for i in numberRange:
            classId=request.POST.get(f'class{i}')
            classObj = Class.objects.filter(id=classId).first()
            startTimeStr = request.POST.get(f'startTime{i}')
            startTime = datetime.fromisoformat(startTimeStr) if startTimeStr else None
            endTimeStr = request.POST.get(f'endTime{i}')
            endTime = datetime.fromisoformat(endTimeStr) if endTimeStr else None
            type = request.POST.get(f'type{i}')
            Session.objects.create(
                startTime = startTime,
                endTime = endTime,
                type = type,
                # link fields
                shift = shift,
                classObj = classObj,
            )
        sessions = Session.objects.filter(shift=shift)
        user_inf = UserInfo.objects.filter(user=user).first()
        context = {
            'user': user,
            'user_inf': user_inf,
            'term':term,
            'shift':shift,
            'sessions':sessions,
        }
        return render(request, 'page/todolist.html', context)

    return render(request, 'page/openShift.html', context)

def getCreateChapter(request):
    if request.method == 'POST':
        ordinal = request.POST.get('ordinal')
        title = request.POST.get('title')
        link = request.POST.get('link')
        chapter = Chapter.objects.create(
            number = int(ordinal) if ordinal else 0,
            title = title if title else "No title",
            link = link if link else None,
        )
        script = """
            <script >
                window.close(); 
            </script>
        """
        return HttpResponse(script)
    return render(request,'page/createChapter.html')

def get_close_shift(request, id):
    user = User.objects.filter(id=id).first()
    user_inf = UserInfo.objects.filter(user=user).first()
    term = Term.objects.filter(user=user).first()
    shift = Shift.objects.filter(endTime__gt=timezone.now(), user=user).first()
    sessions = Session.objects.filter(shift=shift)
    context = {
        'user':user,
        'user_inf': user_inf,   
        'term':term,
        'shift':shift,
        'sessions':sessions,
        }
    return render(request, 'page/close_shift.html', context)

def getChapters(request):
    if request.method == "GET" and "subjectId" in request.GET:
        subjectId = request.GET["subjectId"]
        subject = get_object_or_404(Subject, id=subjectId)
        chapters = Chapter.objects.filter(subject=subject)
        data = [{"id": chapter.id, "title": chapter.title} for chapter in chapters]
        return JsonResponse({"chapters": data})
    return JsonResponse({"error": "Invalid request"}, status=400)