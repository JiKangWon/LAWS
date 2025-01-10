from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.timezone import make_aware
from datetime import datetime, date, timedelta
import calendar
from django.http import JsonResponse, HttpResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import make_aware
from calendar import monthrange

# Create your views here.

# ! GET LOGIN FORM AND 
def getHome(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        now = datetime.now()
        user = User.objects.filter(username=username, password=password).first()
        user_inf = UserInfo.objects.filter(user=user).first()
        if user:
            context = {
                'user':user,
                'user_inf': user_inf,  
                'now':now,
            }
            return render(request, 'page/home.html', context)
    return render(request, 'log/login.html')

# ! GET TO-DO LIST PAGE:
def get_todolist(request, id):
    user = User.objects.filter(id=id).first()
    user_inf = UserInfo.objects.filter(user=user).first()
    term = Term.objects.filter(user=user).first()
    shift = Shift.objects.filter(status=False, user=user).first()
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
def getOpenShift(request, id, number):
    user = User.objects.filter(id=id).first()
    term = Term.objects.filter(user=user).first()
    classes = Class.objects.filter(term=term)
    numberRange = range(1,number+1)
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
    shift = Shift.objects.filter(status=False, user=user).first()
    sessions = Session.objects.filter(shift=shift)
    context = {
        'user':user,
        'user_inf': user_inf, 
        'now':timezone.now(),  
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
            shift.status = True
            shift.endTime = timezone.now()
            shift.save()
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

# ! GET ADD CONTENT OF CHAPTER PAGE:
def getAddContentOfChapter(request, chapterId):
    chapter = Chapter.objects.filter(id = chapterId).first()
    context = {
        'chapter':chapter,
    }
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        link = request.POST.get('link')
        ContentOfChapters.objects.create(
            title = title,
            link = link,
            content = content,
            chapter = chapter,
        )
        script = """
            <script >
                window.close();
            </script>
        """
        return HttpResponse(script)
    return render(request, 'page/addContentOfChapter.html', context)

# ! GET EDIT OF CHAPTER PAGE:
def getEditChapter(request, chapterId):
    chapter = Chapter.objects.filter(id = chapterId).first()
    contents = ContentOfChapters.objects.filter(chapter = chapter)
    context = {
        'chapter':chapter,
        'contents':contents,
    }
    if request.method == 'POST':
        postOrdinal = request.POST.get('ordinal')
        postTitle = request.POST.get('titleChapter')
        postLink = request.POST.get('linkChapter')
        chapter.number = int(postOrdinal)
        chapter.title = postTitle
        chapter.link = postLink
        chapter.save()
        i=0
        for content in contents:
            i+=1
            postTitle = request.POST.get(f'title{i}')
            postLink = request.POST.get(f'link{i}')
            postContent = request.POST.get(f'content{i}')
            content.title = postTitle
            content.link = postLink
            content.content = postContent
            content.save()
        return getContentOfChapter(request, chapterId)
    return render(request, 'page/editChapter.html', context)

@csrf_exempt
def delContentOfChapter(request, contentId):
    if request.method == "DELETE":
        content = ContentOfChapters.objects.filter(id=contentId).first()
        content.delete()
        return JsonResponse({"message": "Content deleted successfully"}, status=200)
    return JsonResponse({"error": "Invalid request method"}, status=400)

# ! GET MANAGE USER PAGE:
def getUserInformation(request, userId):
    user = User.objects.filter(id=userId).first()
    user_inf = UserInfo.objects.filter(user=user).first()
    terms = Term.objects.filter(user=user)
    context = {
        'user': user,
        'userInfo': user_inf,
        'terms': terms
    }
    return render(request, 'manage/userInformation.html', context)

# ! GET EDIT USER PAGE:
def getEditUserInformation(request, userId):
    user = User.objects.filter(id=userId).first()
    user_inf = UserInfo.objects.filter(user=user).first()
    terms = Term.objects.filter(user=user)
    context = {
        'user': user,
        'userInfo': user_inf,
        'terms': terms,
    }
    if request.method == 'POST':
        postName = request.POST.get('name')
        postEmail = request.POST.get('email')
        possPhoneNumber = request.POST.get('phoneNumber')
        postAddress = request.POST.get('address')
        postDob = request.POST.get('dob')
        dob = datetime.strptime(postDob, '%Y-%m-%d').date()
        postSchool = request.POST.get('school')
        user_inf.name = postName
        user_inf.email = postEmail
        user_inf.phoneNumber = possPhoneNumber
        user_inf.address = postAddress
        user_inf.dob = dob
        user_inf.school = postSchool
        user_inf.save()
        return render(request, 'manage/userInformation.html', context)
    return render(request,'edit/userInformation.html', context)

# ! GET MANAGE TERM PAGE:
def getManageTerm(request, termId):
    term = Term.objects.filter(id=termId).first()
    classes = Class.objects.filter(term=term)
    context = {
        'term': term,
        'classes': classes,
    }
    return render(request, 'manage/term.html', context)

# ! DELETE A TERM BY ID AND DELETE METHOD:
def delTerm(request, termId):
    if request.method == "DELETE":
        # Tìm term với id tương ứng
        term = Term.objects.filter(id=termId).first()
        
        # Kiểm tra xem term có tồn tại không
        if term:
            term.delete()
            return JsonResponse({"message": "Term deleted successfully"}, status=200)
        else:
            return JsonResponse({"error": "Term not found"}, status=404)

    return JsonResponse({"error": "Invalid request method"}, status=400)

def delClass(request, classId):
    if request.method == "DELETE":
        # Tìm class với id tương ứng
        classObj = Class.objects.filter(id=classId).first()
        
        # Kiểm tra xem class có tồn tại không
        if classObj:
            classObj.delete()
            return JsonResponse({"message": "Class deleted successfully"}, status=200)
        else:
            return JsonResponse({"error": "Class not found"}, status=404)
    return JsonResponse({"error": "Invalid request method"}, status=400)

# ! GET CREATE TERM PAGE:
def getCreateTerm(request, userId):
    user = User.objects.filter(id=userId).first()
    userInfo = UserInfo.objects.filter(user=user).first()
    context = {
        'user': user,
        'userInfo': userInfo,
    }
    if request.method == 'POST':
        postName = request.POST.get('name')
        postStartDate = request.POST.get('startDate')
        startDate = datetime.strptime(postStartDate, "%Y-%m-%d").date()
        postEndDate = request.POST.get('endDate')
        endDate = datetime.strptime(postEndDate, "%Y-%m-%d").date()
        postTotalOfMonth = request.POST.get('totalOfMonth')
        totalOfMonths = int(postTotalOfMonth)
        term = Term.objects.create(
            name = postName,
            startDate = startDate,
            endDate = endDate,
            totalOfMonths = totalOfMonths,
            user = user,
        )        
        script = """
            <script >
                window.close();
            </script>
        """
        return HttpResponse(script)
    return render(request, 'create/term.html', context)

# ! GET EDIT TERM PAGE:
def getEditTerm(request, termId):
    term = Term.objects.filter(id= termId).first()
    classes = Class.objects.filter(term=term)
    context = {
        'term':term,
        'classes':classes,
    }
    if request.method == 'POST':
        postName = request.POST.get('name')
        postStartDate = request.POST.get('startDate')
        startDate = datetime.strptime(postStartDate, "%Y-%m-%d").date()
        postEndDate = request.POST.get('endDate')
        endDate = datetime.strptime(postEndDate, "%Y-%m-%d").date()
        postTotalOfMonth = request.POST.get('totalOfMonths')
        totalOfMonths = int(postTotalOfMonth)
        term.name = postName
        term.startDate = startDate
        term.endDate = endDate
        term.totalOfMonths = totalOfMonths
        term.save()
        return getManageTerm(request, termId)
    return render(request, 'edit/term.html', context)

# ! GET CREATE CLASS PAGE:
def getCreateClass(request, termId):
    term = Term.objects.filter(id=termId).first()
    context = {
        'term':term,
    }
    if request.method == 'POST':
        postName = request.POST.get('name')
        postStartDate = request.POST.get('startDate')
        startDate = datetime.strptime(postStartDate, "%Y-%m-%d").date()
        postEndDate = request.POST.get('endDate')
        endDate = datetime.strptime(postEndDate, "%Y-%m-%d").date()
        postStatus = request.POST.get('status')
        postMaxOfDay = request.POST.get('maxOfDay')
        maxOfDay = int(postMaxOfDay)
        postMaxOfSessionsInDay = request.POST.get('maxOfSessionsInDay')
        maxOfSessionsInDay = int(postMaxOfSessionsInDay)
        newClass = Class.objects.create(
            name = postName,
            startDate = startDate,
            endDate = endDate,
            status = postStatus,
            term = term,
            maxOfDay = maxOfDay,
            maxOfSessionsInDay = maxOfSessionsInDay,
        )
        initPathway(newClass.id)
        script = """
            <script >
                window.close();
            </script>
        """
        return HttpResponse(script)
    return render(request, 'create/class.html', context)

# ! GET CLASS MANAGEMENT PAGE:
def getManageClass(request, classId):
    classObj = Class.objects.filter(id=classId).first()
    subjects = Subject.objects.filter(class_object = classObj)
    context = {
        'class':classObj,
        'subjects': subjects,
    }
    return render(request, 'manage/class.html', context)

# ! GET EDIT CLASS PAGE:
def getEditClass(request, classId):
    classObj = Class.objects.filter(id=classId).first()
    subjects = Subject.objects.filter(class_object = classObj)
    context = {
        'class':classObj,
        'subjects': subjects,
    }
    if request.method == 'POST':
        postName = request.POST.get('name')
        postStartDate = request.POST.get('startDate')
        startDate = datetime.strptime(postStartDate, "%Y-%m-%d").date()
        postEndDate = request.POST.get('endDate')
        endDate = datetime.strptime(postEndDate, "%Y-%m-%d").date()
        postStatus = request.POST.get('status')
        classObj.name = postName
        classObj.startDate = startDate
        classObj.endDate = endDate
        classObj.status = postStatus
        classObj.save()
        return getManageClass(request, classId)
    return render(request, 'edit/class.html', context)

# ! GET CREATE SUBJECT PAGE:
def getCreateSubject(request, classId):
    classObj = Class.objects.filter(id=classId).first()
    context = {
        'class':classObj,
    }
    if request.method == 'POST':
        postName = request.POST.get('name')
        Subject.objects.create(
            name = postName,
            class_object = classObj,
        )
        script = """
            <script >
                window.close();
            </script>
        """
        return HttpResponse(script)
    return render(request, 'create/subject.html', context)

# ! DELETE A SUBJECT:
def delSubject(request, subjectId):
    if request.method == "DELETE":
        # Tìm subject với id tương ứng
        subject = Subject.objects.filter(id=subjectId).first()
        # Kiểm tra xem subject có tồn tại không
        if subject:
            subject.delete()
            return JsonResponse({"message": "Subject deleted successfully"}, status=200)
        else:
            return JsonResponse({"error": "Subject not found"}, status=404)
    return JsonResponse({"error": "Invalid request method"}, status=400)

# ! GET MANAGE SUBJECT PAGE:

def getManageSubject(request, subjectId):
    subject = Subject.objects.filter(id=subjectId).first()
    chapters = Chapter.objects.filter(subject=subject)
    chapter_with_contents = [
        {
            'chapter': chapter,
            'contents': ContentOfChapters.objects.filter(chapter=chapter)
        }
        for chapter in chapters
    ]
    context = {
        'subject': subject,
        'chapter_with_contents': chapter_with_contents,
    }
    return render(request, 'manage/subject.html', context)
# ! GET EDIT SUBJECT PAGE:
def getEditSubject(request, subjectId):
    subject = Subject.objects.filter(id=subjectId).first()
    chapters = Chapter.objects.filter(subject=subject)
    chapter_with_contents = [
        {
            'chapter': chapter,
            'contents': ContentOfChapters.objects.filter(chapter=chapter)
        }
        for chapter in chapters
    ]
    context = {
        'subject': subject,
        'chapter_with_contents': chapter_with_contents,
    }
    if request.method == 'POST':
        postName = request.POST.get('name')
        subject.name = postName
        subject.save()
        return getManageSubject(request, subjectId)
    return render(request, 'edit/subject.html', context)

# ! INIT PATHWAY FOR A CLASS: 
def initPathway(classId):
    classObj = Class.objects.filter(id=classId).first()
    for i in range(1,classObj.maxOfDay+1):
        newDay = DayPathway.objects.create(
            ordinal = i,
            classObj = classObj
        )
        if i%2==0:
            SessionPathway.objects.create(
                type = "practice",
                content = "Luyện tập tổng hợp",
                iCode = "PRAC",
                ordinal = i/2,
                day = newDay,
            )

# ! GET PATHWAY MANAGEMENT PAGE:
def getPathway(request, classId):
    classObj = Class.objects.filter(id=classId).first()
    days = DayPathway.objects.filter(classObj=classObj)
    days_with_sessions = [
        {
            'day': day,
            'sessions': SessionPathway.objects.filter(day=day)
        }
        for day in days
    ]
    rows = [days_with_sessions[i:i + 7] for i in range(0, len(days_with_sessions), 7)]
    context = {
        'class':classObj,
        'days_with_sessions': days_with_sessions,
        'rows': rows,
    }
    return render(request, 'manage/pathway.html', context)

def getDeltaOrdinal(index):
    if index == 0 or index == 1:
        return index
    if index == 2:
        return 3
    return 3.5 * (index - 1.5 + (-0.5 if index % 2 == 0 else 0.5))

# ! GET CREATE SESSION PAGE:

def getCreateSession(request, dayId):
    day = DayPathway.objects.filter(id=dayId).first()
    classObj = day.classObj
    context = {
        'day':day,
    }
    if request.method == 'POST':
        postContent = request.POST.get('content')
        postICode = request.POST.get('iCode')
        newSession = SessionPathway.objects.create(
            content = postContent,
            iCode = postICode,
            day = day,
        )
        i=0
        dayOrdinal = day.ordinal
        while(True):
            i+=1
            dayOrdinal += getDeltaOrdinal(i)
            if dayOrdinal > day.getMaxDay():
                break
            temp = dayOrdinal
            while (classObj.isFull(temp)):
                temp += 1
            day = classObj.getDayPathway(temp)
            newSession = SessionPathway.objects.create(
                type = "review",
                content = postContent,
                day = day,
                iCode = postICode,
                ordinal = i,
            )

        script = """
            <script >
                window.close();
            </script>
        """
        return HttpResponse(script)
    return render(request, 'create/session.html', context)

# ! DELETE SESSIONS:

def delSessions(request, sessionId):
    if request.method == "DELETE":
        # Tìm session với id tương ứng
        session = SessionPathway.objects.filter(id=sessionId).first()
        # Kiểm tra xem session có tồn tại không
        if session:
            sessions = SessionPathway.objects.filter(iCode=session.iCode, ordinal__gt=session.ordinal).delete()
            session.delete()
            return JsonResponse({"message": "Session deleted successfully"}, status=200)
        else:
            return JsonResponse({"error": "Session not found"}, status=404)
    return JsonResponse({"error": "Invalid request method"}, status=400)

def changeSessionStatus(request, sessionId):
    if request.method == "PUT":
        # Tìm session với id tương ứng
        session = SessionPathway.objects.filter(id=sessionId).first()
        # Kiểm tra xem session có tồn tại không
        if session:
            session.status = not session.status
            session.save()
            return JsonResponse({"message": "Session status changed successfully"}, status=200)
        else:
            return JsonResponse({"error": "Session not found"}, status=404)
    return JsonResponse({"error": "Invalid request method"}, status=400)

# ! GET HISTORY OF CLASS:
def getHistoryOfClass(request, classId, year, month):
    classObj = get_object_or_404(Class, id=classId)
    
    # TODO: Lấy tất cả các buổi học trong tháng
    sessions = Session.objects.filter(
        classObj=classObj,
        startTime__year=year,
        startTime__month=month
    ).order_by('startTime')
    
    # TODO: tạo một dict lưu thông tin với key = session_date và value = list(session)
    sessions_by_date = {}
    for session in sessions:
        session_date = session.startTime.date()
        if session_date not in sessions_by_date:
            sessions_by_date[session_date] = []
        sessions_by_date[session_date].append(session)
    
    # TODO: Tạo cấu trúc lịch
    first_day_of_month = date(year, month, 1)
    _, days_in_month = calendar.monthrange(year, month)
    month_dates = [first_day_of_month + timedelta(days=i) for i in range(days_in_month)]
    
    weeks = []
    first_weekday = first_day_of_month.weekday()  # 0 = Thứ Hai, ..., 6 = Chủ Nhật
    week = [''] * first_weekday  # Thêm ngày trống cho tuần đầu tiên
    
    for day in month_dates:
        week.append({
            "day": day,
            "sessions": sessions_by_date.get(day, [])
        })
        if len(week) == 7:
            weeks.append(week)
            week = []
    if week:  # Thêm tuần còn lại nếu chưa đủ 7 ngày
        while len(week) != 7:
            week.append({})
        weeks.append(week)
    
    context = {
        'class': classObj,
        'weeks': weeks,
        'year': year,
        'month': month,
    }
    return render(request, 'history/class.html', context)
    
# ! GET HISTORY OF SUBJECT:
def getHistoryOfSubject(request, subjectId, month, year):
    subject = get_object_or_404(Subject, id=subjectId)
    
    # TODO: Lấy tất cả các bu��i học trong tháng
    sessions = Session.objects.filter(
        subject=subject,
        startTime__year=year,
        startTime__month=month
    ).order_by('startTime')
    
    # TODO: tạo một dict lưu thông tin với key = session_date và value = list(session)
    sessions_by_date = {}
    for session in sessions:
        session_date = session.startTime.date()
        if session_date not in sessions_by_date:
            sessions_by_date[session_date] = []
        sessions_by_date[session_date].append(session)
    
    # TODO: Tạo cấu trúc lịch
    first_day_of_month = date(year, month, 1)
    _, days_in_month = calendar.monthrange(year, month)
    month_dates = [first_day_of_month + timedelta(days=i) for i in range(days_in_month)]
    
    weeks = []
    first_weekday = first_day_of_month.weekday()  # 0 = Thứ Hai, ..., 6 = Chủ Nhật
    week = [''] * first_weekday  # Thêm ngày trống cho tuần đầu tiên
    
    for day in month_dates:
        week.append({
            "day": day,
            "sessions": sessions_by_date.get(day, [])
        })
        if len(week) == 7:
            weeks.append(week)
            week = []
    if week:  # Thêm tuần còn lại nếu chưa đ�� 7 ngày
        while len(week) != 7:
            week.append({})
        weeks.append(week)
    
    context = {
        'subject': subject,
        'weeks': weeks,
        'year': year,
        'month': month,
    }
    return render(request, 'history/subject.html', context)

def getHistoryOfShift(request,userId, month, year):
    user = User.objects.filter(id=userId).first()
    shifts = Shift.objects.filter(
        user = user,
        startTime__year=year,
        startTime__month=month
    ).order_by('startTime')

    shift_by_date = {}
    for shift in shifts:
        shift_date = shift.startTime.date()
        if shift_date not in shift_by_date:
            shift_by_date[shift_date] = []
        shift_by_date[shift_date].append(shift)

    first_day_of_month = date(year, month, 1)
    _, days_in_month = calendar.monthrange(year, month)
    month_dates = [first_day_of_month + timedelta(days=i) for i in range(days_in_month)]

    weeks = []
    first_weekday = first_day_of_month.weekday()  # 0 = Thứ Hai, ..., 6 = Chủ Nhật
    week = [''] * first_weekday  # Thêm ngày trống cho tuần đầu tiên
    
    for day in month_dates:
        week.append({
            "day": day,
            "shifts": shift_by_date.get(day, [])
        })
        if len(week) == 7:
            weeks.append(week)
            week = []
    if week:  # Thêm tuần còn lại nếu chưa đ�� 7 ngày
        while len(week) != 7:
            week.append({})
        weeks.append(week)
    
    context = {
        'user': user,
        'userInfo': UserInfo.objects.filter(user=user).first(),
        'weeks': weeks,
        'year': year,
        'month': month,
    }
    return render(request, 'history/shift.html', context)

# ! GET FINANCE MANAGEMENT PAGE:
def getFinance(request, userId, month, year):
    user = User.objects.filter(id=userId).first()
    funds = Fund.objects.filter(user=user)
    funds_total = sum(fund.value for fund in funds)
    userInfo = UserInfo.objects.filter(user=user).first()
    typesOfTransaction = TypeOfTransaction.objects.filter(user=user, month=month, year=year)
    transactions = Transaction.objects.filter(user=user, date__month=month, date__year=year)
    income_types = [type for type in typesOfTransaction if type.maxValue > 0]
    expense_types = [type for type in typesOfTransaction if type.maxValue < 0]

    prev_balance = user.balance

    it = []
    for incomeType in income_types:
        val = incomeType.getValue(month, year)
        it.append({
            'income_type':incomeType,
            'value': val,
        })
        prev_balance -= val
    et = []
    for expenseType in expense_types:
        val = expenseType.getValue(month, year)
        et.append({
            'expense_type': expenseType,
            'value': val,
        })
        prev_balance -= val
    

    
    context = {
        'user': user,
        'userInfo': userInfo,
        'typesOfTransaction':typesOfTransaction,
        'transactions': transactions,
        'income_types': it,
        'expense_types': et,
        'year': year,
        'month': month,
        'prev_balance':prev_balance,
        'funds': funds,
        'deltaBalance': funds_total - user.balance,
    }
    return render(request, 'finance/finance.html', context)

def getCreateTypePos(request, userId, month, year):
    user = User.objects.filter(id = userId).first()
    if request.method == 'POST':
        postName = request.POST.get('name')
        postMaxValue = request.POST.get('maxValue')
        maxValue = int(postMaxValue)
        newType = TypeOfTransaction.objects.create(
            user = user,
            name = postName,
            maxValue = maxValue,
            month = month, 
            year = year,
        )
        script = """
            <script >
                window.close();
            </script>
        """
        return HttpResponse(script)
    return render(request, 'finance/createTypePos.html')

def getCreateTypeNeg(request, userId, month, year):
    user = User.objects.filter(id = userId).first()
    if request.method == 'POST':
        postName = request.POST.get('name')
        postMaxValue = request.POST.get('maxValue')
        maxValue = int(postMaxValue)
        newType = TypeOfTransaction.objects.create(
            user = user,
            name = postName,
            maxValue = -maxValue
        )
        script = """
            <script >
                window.close();
            </script>
        """
        return HttpResponse(script)
    return render(request, 'finance/createTypeNeg.html')

def getCreateTransaction(request, userId):
    user = User.objects.filter(id = userId).first()
    typesOfTransaction = TypeOfTransaction.objects.filter(user=user)
    context = {
        'user': user,
        'types': typesOfTransaction,
    }
    if request.method == 'POST':
        postName = request.POST.get('title')
        postValue = request.POST.get('value')
        postType = request.POST.get('type')
        value = int(postValue)
        typeId = int(postType)
        date = timezone.now()
        type = TypeOfTransaction.objects.filter(id=typeId).first()
        newTransaction = Transaction.objects.create(
            user = user,
            title = postName,
            value = value,
            type = type,
            date = date,
        )
        user.balance += value
        user.save()
        script = """
            <script >
                window.close();
            </script>
        """
        return HttpResponse(script)
    return render(request, 'finance/createTransaction.html', context)

def getHistoryOfTransaction(request, userId):
    user = User.objects.filter(id = userId).first()
    transactions = Transaction.objects.filter(user=user).order_by('-date')
    context = {
        'user': user,
        'transactions': transactions,
    }
    return render(request, 'finance/history.html', context)

def reportFinance(request, userId, month, year):
    user = User.objects.filter(id = userId).first()
    transactions = Transaction.objects.filter(user=user, date__month=month, date__year=year).order_by('date')
    transactions_by_dates = {}
    for transaction in transactions:
        transaction_date = transaction.date
        if transaction_date not in transactions_by_dates:
            transactions_by_dates[transaction_date] = []
        transactions_by_dates[transaction_date].append(transaction)
    
    first_day_of_month = date(year, month, 1)
    _, days_in_month = calendar.monthrange(year, month)
    month_dates = [first_day_of_month + timedelta(days=i) for i in range(days_in_month)]

    weeks = []
    first_weekday = first_day_of_month.weekday()  # 0 = Thứ Hai, ..., 6 = Chủ Nhật
    week = [''] * first_weekday  # Thêm ngày trống cho tuần đầu tiên

    for day in month_dates:
        transactionList = transactions_by_dates.get(day, [])
        total_sum = sum(transaction.value for transaction in transactionList)
        week.append({
            "day": day,
            "transactions": transactionList,
            "sum": total_sum,
        })
        if len(week) == 7:
            weeks.append(week)
            week = []
    if week:  # Thêm tuần còn lại nếu chưa đ�� 7 ngày
        while len(week) != 7:
            week.append({})
        weeks.append(week)
    
    context = {
        'user': user,
        'userInfo': UserInfo.objects.filter(user=user).first(),
        'weeks': weeks,
        'year': year,
        'month': month,
    }
    return render(request, 'finance/report.html', context=context)

    
def getHistoryOfShift(request,userId, month, year):
    user = User.objects.filter(id=userId).first()
    shifts = Shift.objects.filter(
        user = user,
        startTime__year=year,
        startTime__month=month
    ).order_by('startTime')

    shift_by_date = {}
    for shift in shifts:
        shift_date = shift.startTime.date()
        if shift_date not in shift_by_date:
            shift_by_date[shift_date] = []
        shift_by_date[shift_date].append(shift)

    first_day_of_month = date(year, month, 1)
    _, days_in_month = calendar.monthrange(year, month)
    month_dates = [first_day_of_month + timedelta(days=i) for i in range(days_in_month)]

    weeks = []
    first_weekday = first_day_of_month.weekday()  # 0 = Thứ Hai, ..., 6 = Chủ Nhật
    week = [''] * first_weekday  # Thêm ngày trống cho tuần đầu tiên
    
    for day in month_dates:
        week.append({
            "day": day,
            "shifts": shift_by_date.get(day, [])
        })
        if len(week) == 7:
            weeks.append(week)
            week = []
    if week:  # Thêm tuần còn lại nếu chưa đ�� 7 ngày
        while len(week) != 7:
            week.append({})
        weeks.append(week)
    
    context = {
        'user': user,
        'userInfo': UserInfo.objects.filter(user=user).first(),
        'weeks': weeks,
        'year': year,
        'month': month,
    }
    return render(request, 'history/shift.html', context)

def delType(request, typeId):
    if request.method == 'DELETE':
        type = TypeOfTransaction.objects.filter(id=typeId).first()
        if type:
            type.delete()
            return HttpResponse(status=204)
        return HttpResponse(status=404)

def getEditTypeIn(request, typeId):
    type = TypeOfTransaction.objects.filter(id=typeId).first()
    if request.method == 'POST':
        postName = request.POST.get('name')
        postMaxValue = request.POST.get('maxValue')
        maxValue = int(postMaxValue)
        if type:
            type.name = postName
            type.maxValue = maxValue
            type.save()
            script = """
                <script >
                    window.close();
                </script>
            """
            return HttpResponse(script)
        return HttpResponse(status=404)
    return render(request, 'finance/editTypeIn.html', {'type': type})

def getEditTypeOut(request, typeId):
    type = TypeOfTransaction.objects.filter(id=typeId).first()
    if request.method == 'POST':
        postName = request.POST.get('name')
        postMaxValue = request.POST.get('maxValue')
        maxValue = int(postMaxValue)
        if type:
            type.name = postName
            type.maxValue = -maxValue
            type.save()
            script = """
                <script>
                    window.close();
                </script>
            """
            return HttpResponse(script)
        return HttpResponse(status=404)
    return render(request, 'finance/editTypeOut.html', {'type': type})

def delTransaction(request, transactionId):
    if request.method == 'DELETE':
        transaction = Transaction.objects.filter(id=transactionId).first()
        if transaction:
            transaction.user.balance -= transaction.value
            transaction.user.save()
            transaction.delete()
            return HttpResponse(status=204)
        return HttpResponse(status=404)
    
def createFund(request, userId):
    user = User.objects.filter(id=userId).first()
    if request.method == 'POST':
        postName = request.POST.get('name')
        postValue = request.POST.get('value')
        value = int(postValue)
        Fund.objects.create(
            user = user,
            name = postName,
            value = value,
        )
        script = """
            <script>
                window.close();
            </script>
        """
        return HttpResponse(script)
    return render(request, 'finance/createFund.html')

def updateFunds(request, userId):
    user = User.objects.filter(id=userId).first()
    funds = Fund.objects.filter(user=user)
    if request.method == 'POST':
        for fund in funds:
            postValue = request.POST.get(f'fund{fund.id}')
            value = int(postValue)
            fund.value = value
            fund.save()
        script = """
            <script>
                window.close();
            </script>
        """
        return HttpResponse(script)
    return render(request, 'finance/updateFunds.html', {'funds': funds})

def getRegister(request):
    if request.method == 'POST':
        postUsername = request.POST.get('username')
        postPassword = request.POST.get('password')
        postName = request.POST.get('name')
        postEmail = request.POST.get('email')
        postPhoneNumber = request.POST.get('phoneNumber')
        postAddress = request.POST.get('address')
        postDob = request.POST.get('dob')
        dob = datetime.strptime(postDob, '%Y-%m-%d')
        postSchool = request.POST.get('school')
        user = User.objects.create(
            username = postUsername,
            password = postPassword,
        )
        UserInfo.objects.create(
            user = user,
            name = postName,
            email = postEmail,
            phoneNumber = postPhoneNumber,
            address = postAddress,
            dob = dob,
            school = postSchool,
        )
        return getHome(request)
    return render(request, 'log/register.html')

def getChangePassword(request, userId):
    user = User.objects.filter(id=userId).first()
    if request.method == 'POST':
        postNewPassword = request.POST.get('password')
        user.password = postNewPassword
        user.save()
        return getHome(request)
    return render(request, 'log/changePassword.html', {'user':user})

# ! DIARY MANAGEMENT:
def getDiary(request, userId):
    user = User.objects.filter(id=userId).first()
    userInfo = UserInfo.objects.filter(user=user).first()
    diaries = Diary.objects.filter(user=user).order_by('-date')
    context = {
        'user':user,
        'userInfo':userInfo,
        'diaries': diaries,
    }
    return render(request, 'page/diary.html', context)
def createDiary(request, userId):
    user = User.objects.filter(id=userId).first()
    context = {
        'user': user,
    }
    if request.method == "POST":
        postTitle = request.POST.get('title')
        postContent = request.POST.get('content')
        diary = Diary.objects.create(
            user = user,
            title = postTitle,
            content = postContent,
        )
        script = """
            <script >
                window.close();
            </script>
        """
        return HttpResponse(script)
    return render(request, 'create/diary.html', context)
def deleteDiary(request, diaryId):
    if request.method == 'DELETE':
        diary = Diary.objects.filter(id=diaryId).first()
        if diary:
            diary.delete()
            return HttpResponse(status=204)
        return HttpResponse(status=404)
def editDiary(request, diaryId):
    diary = Diary.objects.filter(id=diaryId).first()
    context = {
        'user': diary.user,
        'diary': diary,
    }
    if request.method == "POST":
        postTitle = request.POST.get('title')
        postContent = request.POST.get('content')
        diary.title = postTitle
        diary.content = postContent
        diary.save()
        script = """
            <script >
                window.close();
            </script>
        """
        return HttpResponse(script)
    return render(request, 'edit/diary.html', context)

# ! DEADLINE MANAGEMENT:
def getDeadline(request, userId):        
    user = User.objects.filter(id=userId).first()
    deadlines = Deadline.objects.filter(user=user)
    context = {
        'user': user,
        'deadlines':deadlines,
    }
    return render(request, 'page/deadline.html', context)

def delDeadline(request, deadlineId):
    if request.method == 'DELETE':
        deadline = Deadline.objects.filter(id=deadlineId).first()
        if deadline:
            deadline.delete()
            return HttpResponse(status=204)
        return HttpResponse(status=404)
    

def createDeadline(request, userId):
    user = User.objects.filter(id=userId).first()
    context = {
        'user':user,
    }
    if request.method == "POST":
        postContent = request.POST.get('content')
        postDate = request.POST.get('date')
        deadline = Deadline.objects.create(
            user = user,
            content = postContent,
            date = datetime.fromisoformat(postDate),
        )
        script = """
            <script >
                window.close();
            </script>
        """
        return HttpResponse(script)
    return render(request, 'create/deadline.html', context)
    
def delChapter(request, chapterId):
    if request.method == 'DELETE':
        chapter = Chapter.objects.filter(id=chapterId).first()
        if chapter:
            chapter.delete()
            return HttpResponse(status=204)
        return HttpResponse(status=404)
        
