from django.db import models
from django.utils.timezone import localtime

# Create your models here.
class User(models.Model):
    # ! Fields
    username = models.CharField(max_length=30, unique=True, verbose_name='Tên đăng nhập')
    password = models.CharField(max_length=100, verbose_name='Mật khẩu')
    balance = models.IntegerField(verbose_name="Balance", default=0, null=True, blank=True) 

    # ! Methods
    def __str__(self):
        return self.username
    def getStartPassword(self):
        return len(self.password)*'*'
    def getUserInfo(self):
        userInfo = UserInfo.objects.filter(user = self)
        return userInfo
    
class Diary(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Deadline(models.Model):
    content = models.TextField()
    date = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Fund(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    value = models.IntegerField()

class UserInfo(models.Model):
    # ! Fields
    name = models.CharField(max_length=50, verbose_name='Họ và tên')
    email = models.EmailField(unique=True, null=True, verbose_name='Email')
    phoneNumber = models.CharField(max_length=15, null=True, verbose_name='Số điện thoại')
    address = models.CharField(max_length=255, null=True, verbose_name='Địa chỉ')
    dob = models.DateField(verbose_name='Ngày sinh', null=True)
    school = models.CharField(max_length=50, null=True, verbose_name='Thông tin trường học')

    # todo: Link field
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='info', verbose_name='Tài khoản người dùng')

    #! Method
    def __str__(self):
        return self.name

class Term(models.Model):
    # ! Fields
    name = models.CharField(max_length=50, verbose_name='Tên kỳ học')
    startDate = models.DateField(verbose_name='Ngày bắt đầu')
    endDate = models.DateField(verbose_name='Ngày kết thúc', null=True, blank=True)
    totalOfMonths = models.IntegerField(verbose_name='Tổng số tháng dự kiến cho học kỳ')

    # todo: Link field
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='Thông tin người dùng')
    
    # ! Methods
    def __str__(self):
        return self.name

class Class(models.Model):
    STATUS_CHOICES = (
        ('active','active'),
        ('upcoming','upcoming'),
        ('completed','completed'),
    )

    # ! Fields
    name = models.CharField(max_length=50, verbose_name='Tên lớp')
    startDate = models.DateField(verbose_name='Thời gian mở lớp', null=True)
    endDate = models.DateField(verbose_name='Thời gian đóng lớp', null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='upcoming')
    maxOfDay = models.IntegerField(verbose_name='Số lượng ngày học tối đa trong kỳ', default=50)
    maxOfSessionsInDay = models.IntegerField(verbose_name="Số lượng buổi học tối đa trong ngày", default=2)
    # todo: Link fields
    term = models.ForeignKey(Term, on_delete=models.CASCADE, verbose_name='Thông tin kỳ học')

    # ! Methods
    def __str__(self):
        return self.name
    def getSubjectList(self):
        return Subject.objects.filter(class_object = self)
    def getDifferentStatus(self):
        statuses = ['active', 'upcoming', 'completed']
        statuses.remove(self.status)
        return statuses
    @property
    def getDaysPathWay(self):
        days = DayPathway.objects.filter(classObj = self)
        return days
    def getDayPathway(self, ordinal):
        return DayPathway.objects.filter(classObj = self, ordinal=ordinal).first()
    def isFull(self, ordinal):
        return self.getDayPathway(ordinal).isFull()

class Subject(models.Model):
    # ! Fields
    name = models.CharField(max_length=50, verbose_name='Tên môn học')
    
    # todo: Link fields
    class_object = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name='Lớp chứa môn học') 
    
    # ! Methods
    def get_history_of_sessions(self):
        pass
    def __str__(self):
        return self.name

class Course(models.Model):
    # ! Fields
    name = models.CharField(max_length=200, null=True, verbose_name='Tên khóa học')
    teacher = models.CharField(max_length=200, null=True, verbose_name='Tên giảng viên')
    link = models.URLField(max_length=250,verbose_name='Nguồn khóa học')

    # todo: Link fields
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE, null=True, verbose_name='Thông tin môn học của khóa')

    # ! Methods
    def __str__(self):
        return self.name

class Shift(models.Model):
    # ! Fields
    name = models.CharField(max_length=50, verbose_name='Name of Shift ')
    startTime = models.DateTimeField(auto_now_add=True, verbose_name='Start time of Shift')
    endTime = models.DateTimeField(null=True, blank=True, verbose_name='End time of Shift')
    status = models.BooleanField(default=False, verbose_name='Status')

    # todo: Link fields
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User of this Shift', null=True)

    # ! Methods

    # todo: ToString method
    def __str__(self):
        return self.name
    
    # todo: Count method
    def get_number_of_sessions(self):
        sessions = Session.objects.filter(shift = self)
        return sessions.count()
    
    @property
    def getSessions(self):
        return Session.objects.filter(shift = self)

class Chapter(models.Model):
    # ! Fields
    title = models.CharField(max_length=250, verbose_name='Title')
    number = models.IntegerField(verbose_name='Ordinal Number')
    link = models.URLField(max_length=250,verbose_name='Link to Theory File', null=True)

    # todo: Link fields
    subject = models.ForeignKey(Subject,null=True, on_delete=models.CASCADE, verbose_name='Subject of this chapter')

    # ! Methods

    # todo: ToString method
    def __str__(self):
        return f"Chương {self.number}. {self.title}"

class Session(models.Model):

    TYPE_CHOICES = (
        ('learn','learn'),
        ('review','review'),
        ('practice','practice')
    )

    # ! Fields

    startTime = models.DateTimeField(verbose_name='Start Time')
    endTime = models.DateTimeField(verbose_name='End Time')
    type = models.CharField(max_length=10,choices=TYPE_CHOICES, default='learn')
    note = models.TextField(verbose_name="Note",null=True, blank=True)
    
    # todo: link fields
    shift = models.ForeignKey(Shift,on_delete=models.CASCADE, null=True, blank=True, verbose_name='Shift for this Session')
    classObj = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Class in this session')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Subject in this session')
    chapter = models.ManyToManyField(Chapter,blank=True, verbose_name="Chapter in this session")

    # ! Methods:
    
    # todo: To String Methods
    def __str__(self):
        return f"Buổi học môn {self.subject.name}" if self.subject else f"Không xác định khóa học"
    def getDate(self):
        return self.startTime.date()

    # todo: format for start and end
    def getStart(self):
        return localtime(self.startTime).strftime('%Y-%m-%dT%H:%M')
    def getEnd(self):
        return localtime(self.endTime).strftime('%Y-%m-%dT%H:%M')
    
    # todo: get different choices for processing close shift
    def getDifferentChoices(self):
        typeChoices = ['learn', 'review', 'practice']
        typeChoices.remove(self.type)
        return typeChoices
    
class ContentOfChapters(models.Model):

    # ! Fields:

    title = models.TextField(max_length=250, verbose_name='Title')
    content = models.TextField(verbose_name='Content')
    link = models.URLField(max_length=250,verbose_name='Link to Tutorial')

    # Todo: Link fields
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, verbose_name='Chapter of this Content')

    # ! Methods:

    # todo: To String Method
    def __str__(self):
        return f"{self.title}"

class Document(models.Model):

    # ! Fields:
    title = models.CharField(max_length=250, verbose_name='Tiêu đề tài liệu')
    link = models.URLField(max_length=250,verbose_name='Liên kết', null=True)
    file = models.FileField(upload_to='uploads/', null=True, blank=True)

    # Todo: Link fields
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Thông tin môn học')
    
    # ! Methods:

    # todo: To String Method
    def __str__(self):
        return self.title

class TypeOfTransaction(models.Model):
    # ! Fields:
    name = models.CharField(max_length=50, verbose_name='Tên loại giao dịch')
    maxValue = models.IntegerField(verbose_name="Hạn mức tối đa mỗi tháng")
    month = models.IntegerField(default=1)
    year = models.IntegerField(verbose_name='Năm', default=2025)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def getValue(self, month, year):
        transactions = Transaction.objects.filter(type=self, date__month = month, date__year = year)
        totalValue = sum([transaction.value for transaction in transactions])
        return totalValue
    
    @property
    def getAbs(self):
        return abs(self.maxValue)
        


class Transaction(models.Model):

    # ! Fields:
    
    date = models.DateField()
    title = models.CharField(max_length=200, verbose_name='Nội dung giao dịch')
    value = models.FloatField(verbose_name='Giá trị giao dịch')
    
    # Todo: Link fields:
    type = models.ForeignKey(TypeOfTransaction, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE, null=True, blank=True)
    # ! Methods:

    # Todo: ToString method:
    def __str__(self):
        return f"{self.title} - {self.value}"
    
    # Todo: Get object methods:
    def getUser(self):
        return self.user

class DayPathway(models.Model):
    # ! Fields:
    ordinal = models.IntegerField(verbose_name='Số thứ tự ngày học')
    
    # Todo: Link fields:
    classObj = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name='Thông tin lớp học')

    # ! Methods:
    def getSessions(self):
        sessions = SessionPathway.objects.filter(day = self)
        return sessions
    
    def count(self):
        return len(self.getSessions())
    
    def isFull(self):
        sessions = self.getSessions()
        return len(sessions) == self.classObj.maxOfSessionsInDay

    def getStatus(self):
        sessions = self.getSessions()
        for session in sessions:
            if not session.status:
                return False
        return True

    def __str__(self):
        return  f'Day {self.ordinal}'

    def getMaxDay(self):
        return self.classObj.maxOfDay
    
    def getMaxSession(self):
        return self.classObj.maxOfSessionsInDay
    
class SessionPathway(models.Model):
    TYPE_CHOICES = (
        ('learn','learn'),
        ('review','review'),
        ('practice','practice')
    )
        
    # ! Fields:
    ordinal = models.IntegerField(verbose_name='Số thứ tự của buổi học', default=0)
    status = models.BooleanField(verbose_name="Trạng thái buổi học", default=False)
    content = models.TextField(verbose_name="Content of Session")
    type = models.CharField(max_length=10,choices=TYPE_CHOICES, default='learn')
    iCode = models.CharField(max_length=10,verbose_name="Mã số session")
    
    # todo: link fields:
    day = models.ForeignKey(DayPathway, verbose_name="Day of this session", on_delete=models.CASCADE)

    # ! Methods:
    def __str__(self):
        return f'{self.content} (Buổi {self.ordinal})'
    