from django.db import models
from django.utils.timezone import localtime

# Create your models here.
class User(models.Model):
    # ! Fields
    username = models.CharField(max_length=30, unique=True, verbose_name='Tên đăng nhập')
    password = models.CharField(max_length=100, verbose_name='Mật khẩu')

    # ! Methods
    def __str__(self):
        return self.username

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

class Balance(models.Model):
    # ! Fields
    value = models.FloatField(default=0, verbose_name='Số dư')
    
    # todo: Link field
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='balance', verbose_name='Tài khoản người dùng')

    # ! Methods
    def __str__(self):
        return f"Số dư của {self.user.username}"

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
    startDate = models.DateField(verbose_name='Thời gian mở lớp', null=True, auto_now_add=True)
    endDate = models.DateField(verbose_name='Thời gian đóng lớp', null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='upcoming')

    # todo: Link fields
    term = models.ForeignKey(Term, on_delete=models.CASCADE, verbose_name='Thông tin kỳ học')

    # ! Methods
    def __str__(self):
        return self.name
    def getSubjectList(self):
        return Subject.objects.filter(class_object = self)

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
        return f"Nội dung {self.number}. {self.title}"

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

class Transaction(models.Model):

    TYPE_CHOICES = (
        ('monthly_income','monthly income'),
        ('salary','salary'),
        ('other_earnings','other earnings'),
        ('food expenses','food expenses'),
        ('transportation_expenses','Transportation expenses'),
        ('entertainment_expenses','entertainment expenses'),
        ('unexpected_expenses','unexpected expenses'),
        ('monthly_rent','monthly rent'),
        ('study_materials_expenses','Study materials Expenses'),
    )

    # ! Fields:
    
    date = models.DateField()
    title = models.CharField(max_length=200, verbose_name='Nội dung giao dịch')
    value = models.FloatField(verbose_name='Giá trị giao dịch')
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, verbose_name='Loại giao dịch', default='unexpected_expenses')
    
    # Todo: Link fields:
    balance = models.ForeignKey(Balance, on_delete=models.CASCADE, verbose_name='Thông tin tài khoản người dùng')

    # ! Methods:

    # Todo: ToString method:
    def __str__(self):
        return f"{self.title} - {self.value}"
    
    # Todo: Get object methods:
    def getUser(self):
        return self.balance.user

