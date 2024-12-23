from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=30, unique=True, verbose_name='Tên đăng nhập')
    password = models.CharField(max_length=100, verbose_name='Mật khẩu')
    def __str__(self):
        return self.username

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='info', verbose_name='Tài khoản người dùng')
    name = models.CharField(max_length=50, verbose_name='Họ và tên')
    email = models.EmailField(unique=True, null=True, verbose_name='Email')
    phone_number = models.CharField(max_length=15, null=True, verbose_name='Số điện thoại')
    address = models.CharField(max_length=255, null=True, verbose_name='Địa chỉ')
    dob = models.DateField(verbose_name='Ngày sinh', null=True)
    school = models.CharField(max_length=50, null=True, verbose_name='Thông tin trường học')
    def __str__(self):
        return self.name

class Balance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='balance', verbose_name='Tài khoản người dùng')
    balance = models.FloatField(default=0, verbose_name='Số dư')
    def __str__(self):
        return f"Số dư của {self.user.username}"

class Term(models.Model):
    name = models.CharField(max_length=50, verbose_name='Tên kỳ học')
    start_date = models.DateField(verbose_name='Ngày bắt đầu')
    end_date = models.DateField(verbose_name='Ngày kết thúc')
    total_of_months = models.IntegerField(verbose_name='Tổng số tháng dự kiến cho học kỳ')
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='Thông tin người dùng')
    def __str__(self):
        return self.name

class Class(models.Model):
    STATUS_CHOICES = (
        ('active','active'),
        ('upcoming','upcoming'),
        ('completed','completed'),
    )
    name = models.CharField(max_length=50, verbose_name='Tên lớp')
    start_time = models.DateField(verbose_name='Thời gian mở lớp', null=True, auto_now_add=True)
    end_time = models.DateField(verbose_name='Thời gian đóng lớp', null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='upcoming')
    term = models.ForeignKey(Term, on_delete=models.CASCADE, verbose_name='Thông tin kỳ học')
    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=50, verbose_name='Tên môn học')
    class_object = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name='Lớp chứa môn học') 
    def get_history_of_sessions(self):
        pass
    def __str__(self):
        return self.name



class Course(models.Model):
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE, null=True, verbose_name='Thông tin môn học của khóa')
    name = models.CharField(max_length=200, null=True, verbose_name='Tên khóa học')
    teacher = models.CharField(max_length=200, null=True, verbose_name='Tên giảng viên')
    link = models.URLField(max_length=250,verbose_name='Nguồn khóa học')
    def __str__(self):
        return self.name

class Shift(models.Model):
    name = models.CharField(max_length=50, verbose_name='Tên ca làm việc')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Thời gian mở ca')
    # Lấy số lượng sessions trong một ca
    def get_number_of_sessions(self):
        sessions = Session.objects.filter(shift = self)
        return sessions.count()
    # Lấy thời gian kết ca
    def get_end(self):
        return self.date + timedelta(minutes=60) * self.get_number_of_sessions()

class Chapter(models.Model):
    title = models.CharField(max_length=250, verbose_name='Tiêu đề chương')
    number = models.IntegerField(verbose_name='Số thứ tự')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Thông tin khóa học của chương')
    link = models.URLField(max_length=250,verbose_name='Link to Theory File', null=True)
    def __str__(self):
        return f"Chương {self.number}. {self.title}"
    def get_next_reviewed_day(self):
        pass
    def get_the_completion_rate(self):
        pass

class Session(models.Model):
    TYPE_CHOICES = (
        ('learn','learn'),
        ('review','review'),
        ('practice','practice')
    )
    Shift = models.ForeignKey(Shift,on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Thời gian bắt đầu')
    type = models.CharField(max_length=10,choices=TYPE_CHOICES, default='practice')
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE, null=True, blank=True)
    chapter = models.ManyToManyField(Chapter, verbose_name="Các chương học trong buổi")
    note = models.TextField(verbose_name="Ghi chú")
    def __str__(self):
        return f"Buổi học khóa {self.course.name} lúc {self.date}" if self.course else f"Không xác định khóa học"
    def get_end(self):
        return self.start + timedelta(minutes=60)

class ContentOfChapters(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, verbose_name='Thông tin chương')
    title = models.CharField(max_length=250, verbose_name='Tiêu đề nội dung')
    content = models.TextField(verbose_name='Nội dung của chương')
    number = models.IntegerField(verbose_name='Số thứ tự đề mục')
    link = models.URLField(max_length=250,verbose_name='Liên kết')
    def __str__(self):
        return f"Nội dung {self.number}. {self.title}"

class Document(models.Model):
    title = models.CharField(max_length=250, verbose_name='Tiêu đề tài liệu')
    link = models.URLField(max_length=250,verbose_name='Liên kết', null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Thông tin môn học')
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
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
    balance = models.ForeignKey(Balance, on_delete=models.CASCADE, verbose_name='Thông tin tài khoản người dùng')
    date = models.DateField()
    title = models.CharField(max_length=200, verbose_name='Nội dung giao dịch')
    value = models.FloatField(verbose_name='Giá trị giao dịch')
    def __str__(self):
        return f"{self.title} - {self.value}"

