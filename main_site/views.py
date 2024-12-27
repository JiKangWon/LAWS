from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.timezone import make_aware
from datetime import datetime
from django.http import JsonResponse, HttpResponse
from .models import *
from django.utils.timezone import make_aware

# Create your views here.

# ! GET LOGIN FORM AND 
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

# ! GET TO-DO LIST PAGE:
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

# ! GET OPEN SHIFT PAGE AND CREATE NEW SHIFT:
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

# ! GET FORM FOR CREATE NEW CHAPTER WHEN LEARNING NEW LESSONS
def getCreateChapter(request, subjectId):
    if request.method == 'POST':
        ordinal = request.POST.get('ordinal')
        title = request.POST.get('title')
        link = request.POST.get('link')
        subject = Subject.objects.filter(id=subjectId).first()
        chapter = Chapter.objects.create(
            number = int(ordinal) if ordinal else 0,
            title = title if title else "No title",
            link = link if link else None,
            subject = subject if subject else None
        )
        script = """
            <script >
                window.close(); 
            </script>
        """
        return HttpResponse(script)
    return render(request,'page/createChapter.html')

# ! GET CLOSE SHIFT PAGE AND CONFIRM INFORMATION OF THAT SHIFT
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
    if request.method == 'POST':
        # todo: get data from request.Post
        i = 0
        for session in sessions:
            i+=1
            postFinished = request.POST.get(f'finish{i}')
            if not postFinished:
                session.delete()
                continue
            postType = request.POST.get(f'type{i}')
            session.type = postType
            postStart = request.POST.get(f'start{i}')
            start = datetime.fromisoformat(postStart) if postStart else None
            session.startTime = make_aware(start)
            postEnd = request.POST.get(f'end{i}')
            end = datetime.fromisoformat(postEnd) if postEnd else None
            session.endTime = make_aware(end)
            postSubject = request.POST.get(f'subject{i}')
            subjectId = int(postSubject)
            subject = Subject.objects.filter(id=subjectId).first()
            session.subject = subject
            postChapters = request.POST.getlist(f'chapter{i}')
            for postChapter in postChapters:
                chapterId = int(postChapter)
                chapter = Chapter.objects.filter(id=chapterId).first()
                session.chapter.add(chapter)
            postNote = request.POST.get(f'note{i}')
            session.note = postNote
            session.save()
        return render(request, 'page/home.html', context)
    return render(request, 'page/close_shift.html', context)

# ! GET CHAPTERS FOR CLOSE SHIFT
def getChapters(request):
    if request.method == "GET" and "subjectId" in request.GET:
        subjectId = request.GET["subjectId"]
        subject = get_object_or_404(Subject, id=subjectId)
        chapters = Chapter.objects.filter(subject=subject)
        data = [{"id": chapter.id, "title": chapter.title} for chapter in chapters]
        return JsonResponse({"chapters": data})
    return JsonResponse({"error": "Invalid request"}, status=400)

# ! GET CONTENT OF CHAPTER:
def getContentOfChapter(request, chapterId):
    chapter = Chapter.objects.filter(id=chapterId).first()
    contents = ContentOfChapters.objects.filter(chapter=chapter)
    context = {
        'chapter':chapter,
        'contents':contents,
    }
    return render(request, 'page/contentOfChapter.html',context)