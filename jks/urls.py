"""
URL configuration for jks project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from main_site import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.getHome, name='home'),
    path('register/', views.getRegister, name='register'),
    path('changePassword/id=<int:userId>/', views.getChangePassword, name='changePassword'),
    path('todo/id=<int:id>/', views.get_todolist, name='todolist'),
    path('todo/open/id=<int:id>/number=<int:number>/', views.getOpenShift, name='open_shift'),
    path('todo/close/id=<int:id>/', views.get_close_shift, name='close_shift'),
    path('models/chapters/create/id=<int:subjectId>/', views.getCreateChapter, name='createChapter'),
    path('getChapters/', views.getChapters, name='getChapters'),
    path('getContentOfChapters/id=<int:chapterId>/', views.getContentOfChapter, name='ContentOfChapter'),
    path('getAddContentOfChapter/id=<int:chapterId>/', views.getAddContentOfChapter, name="AddContentOfChapter"),
    path('getEditChapter/id=<int:chapterId>/', views.getEditChapter, name="EditChapter"),
    path('delContentOfChapter/id=<int:contentId>/', views.delContentOfChapter, name="delContentOfChapter"),
    # ! GET MODELS INFORMATION
    path('manage/userInformation/id=<int:userId>/', views.getUserInformation, name="userInformation"),
    path('manage/term/id=<int:termId>/', views.getManageTerm, name="manageTerm" ),
    path('manage/class/id=<int:classId>/', views.getManageClass, name="manageClass"),
    path('manage/subject/id=<int:subjectId>/', views.getManageSubject, name="manageSubject"),
    path('manage/pathway/id=<int:classId>/', views.getPathway, name="pathway"),
    # ! EDIT MODELS INFORMATION
    path('edit/userInformation/id=<int:userId>/', views.getEditUserInformation, name="editUserInformation"),
    path('edit/term/id=<int:termId>/', views.getEditTerm, name="editTerm"),
    path('edit/class/id=<int:classId>/', views.getEditClass, name="editClass"),
    path('edit/subject/id=<int:subjectId>/', views.getEditSubject, name="editSubject"),
    # ! EDELETE MODELS:
    path('delTerm/id=<int:termId>/', views.delTerm, name="delTerm"),
    path('delClass/id=<int:classId>/', views.delClass, name="delClass"),
    path('delSubject/id=<int:subjectId>/', views.delSubject, name="delSubject"),
    path('delSessions/id=<int:sessionId>/', views.delSessions, name="delSession"),
    path('delChapter/id=<int:chapterId>/', views.delChapter, name="delChapter"),
    # ! CREATE MODELS:
    path('create/term/id=<int:userId>/', views.getCreateTerm, name="createTerm"),
    path('create/class/id=<int:termId>/', views.getCreateClass, name="createClass"),
    path('create/subject/id=<int:classId>/', views.getCreateSubject, name="createSubject"),
    path('create/session/id=<int:dayId>/', views.getCreateSession, name="createSession"),
    # ! PUT METHODS:
    path('put/session/status/id=<int:sessionId>/', views.changeSessionStatus, name="changeSessionStatus" ),
    # ! GET HISTORY:
    path('history/class/id=<int:classId>/month=<int:month>/year=<int:year>/', views.getHistoryOfClass, name="HistoryOfClass"),
    path('history/subject/id=<int:subjectId>/month=<int:month>/year=<int:year>/', views.getHistoryOfSubject, name="HistoryOfSubject"),
    path('history/shift/id=<int:userId>/month=<int:month>/year=<int:year>/', views.getHistoryOfShift, name="HistoryOfShift"),
    # ! FINANCE MANAGEMENT:
    path('finance/id=<int:userId>/month=<int:month>/year=<int:year>/', views.getFinance, name="finance"),
    path('finance/type/create/in/id=<int:userId>/month=<int:month>/year=<int:year>/', views.getCreateTypePos, name="createType"),
    path('finance/type/create/out/id=<int:userId>/month=<int:month>/year=<int:year>/', views.getCreateTypeNeg, name="createType"),
    path('finance/transaction/create/id=<int:userId>/', views.getCreateTransaction, name="createTransaction"),
    path('finance/transaction/history/id=<int:userId>/', views.getHistoryOfTransaction, name="historyOfTransaction"),
    path('finance/transaction/report/id=<int:userId>/month=<int:month>/year=<int:year>/', views.reportFinance, name="reportOfTransaction"),
    path('finance/type/delete/id=<int:typeId>/', views.delType, name="delType"),
    path('finance/transaction/delete/id=<int:transactionId>/', views.delTransaction, name="delTransaction"),
    path('finance/type/edit/in/id=<int:typeId>/', views.getEditTypeIn, name='editTypeIn'),
    path('finance/type/edit/out/id=<int:typeId>/', views.getEditTypeOut, name='editTypeOut'),
    path('finance/fund/create/id=<int:userId>/', views.createFund, name="createFund"),
    path('finance/fund/update/id=<int:userId>/', views.updateFunds, name="updateFunds"),
    # ! DIARY MANAGEMENT:
    path('diary/id=<int:userId>/', views.getDiary, name="diary"),
    path('diary/create/id=<int:userId>/', views.createDiary, name="createDiary"),
    path('diary/delete/id=<int:diaryId>/', views.deleteDiary, name="deleteDiary"),
    path('diary/edit/id=<int:diaryId>/', views.editDiary, name="editDiary"),
    # ! DEADLINE MANAGEMENT:
    path('deadline/id=<int:userId>/', views.getDeadline, name="deadline"),
    path('deadline/create/id=<int:userId>/', views.createDeadline, name="createDeadline"),
    path('deadline/delete/id=<int:deadlineId>/', views.delDeadline, name="deleteDeadline"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
