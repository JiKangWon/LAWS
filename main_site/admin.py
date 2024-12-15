from django.contrib import admin
from .models import *
from django.utils.html import format_html
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'username', 
        'password',
        )
    search_fields = (
        'username',
        )
    list_filter = (
        'username',
        )

@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'user_link',
        'name',
        'email',
        'address',
        'phone_number',
        'dob',
        'school',
    )
    search_fields = (
        'user__username',
        'name',
        'email',
        'address',
        'phone_number',
        'school',
    )
    list_filter = (
        'user__username',
        'dob',
        'phone_number',
        'email',
        'address',
        'name',
    )
    # Thêm một liên kết đến trang User tương ứng
    def user_link(self, obj):
        return format_html('<a href="/admin/{}/{}/{}/change/">{}</a>', 
            obj.user._meta.app_label, 
            obj.user._meta.model_name, 
            obj.user.pk, 
            obj.user.username,
        )    
    user_link.short_description = 'Account'  # Thêm tiêu đề cột

@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user_link',
        'balance'
    )
    def user_link(self, obj):
        user_info = UserInfo.objects.filter(user = obj.user).first()
        return format_html('<a href="/admin/{}/{}/{}/change/">{}</a>', 
            user_info._meta.app_label, 
            user_info._meta.model_name, 
            user_info.pk, 
            user_info.name,
        )    
    user_link.short_description = 'Thông tin người dùng'  # Thêm tiêu đề cột

@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user_link',
        'name',
        'start_date',
        'end_date',
        'total_of_months',
    )
    def user_link(self, obj):
        user_info = UserInfo.objects.filter(user = obj.user).first()
        return format_html('<a href="/admin/{}/{}/{}/change/">{}</a>', 
            user_info._meta.app_label, 
            user_info._meta.model_name, 
            user_info.pk, 
            user_info.name,
        )    
    user_link.short_description = 'Thông tin người dùng'  # Thêm tiêu đề cột

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'start_time',
        'end_time',
        'status',
        'term_link',
    )
    def term_link(self, obj):
        return format_html('<a href="/admin/{}/{}/{}/change/">{}</a>', 
            obj.term._meta.app_label, 
            obj.term._meta.model_name, 
            obj.term.pk, 
            obj.term.name,
        )
    
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'class_link',
    )
    def class_link(self, obj):
        return format_html('<a href="/admin/{}/{}/{}/change/">{}</a>', 
            obj.class_object._meta.app_label, 
            obj.class_object._meta.model_name, 
            obj.class_object.pk, 
            obj.class_object.name,
        )
    
@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'date_of_execution',
        'start',
        'end',
        'type',
        'subject_link',
    )
    def subject_link(self, obj):
        return format_html('<a href="/admin/{}/{}/{}/change/">{}</a>', 
            obj.subject._meta.app_label, 
            obj.subject._meta.model_name, 
            obj.subject.pk, 
            obj.subject.name,
        )

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'teacher',
        'subject_link',
        'link_url',
    )
    def subject_link(self, obj):
        return format_html('<a href="/admin/{}/{}/{}/change/">{}</a>', 
            obj.subject._meta.app_label, 
            obj.subject._meta.model_name, 
            obj.subject.pk, 
            obj.subject.name,
        )
    def link_url(self,obj):
        return format_html('<a href="{}">LINK</a>',obj.link)

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'number',
        'course_link',
    )
    def course_link(self, obj):
        return format_html('<a href="/admin/{}/{}/{}/change/">{}</a>', 
            obj.course._meta.app_label, 
            obj.course._meta.model_name, 
            obj.course.pk, 
            obj.course.name,
        )

@admin.register(ContentOfChapters)
class ContentOfChaptersAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'chapter_link',
        'number',
        'title',
        'content',
        'link_url',
    )
    def chapter_link(self, obj):
        return format_html('<a href="/admin/{}/{}/{}/change/">{}</a>', 
            obj.chapter._meta.app_label, 
            obj.chapter._meta.model_name, 
            obj.chapter.pk, 
            obj.chapter.__str__(),
        )
    def link_url(self,obj):
        return format_html('<a href="{}">LINK</a>',obj.link)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'link_url',
        'file',
        'subject_link',
    )
    def link_url(self,obj):
        return format_html('<a href="{}">LINK</a>',obj.link)
    def subject_link(self, obj):
        return format_html('<a href="/admin/{}/{}/{}/change/">{}</a>', 
            obj.subject._meta.app_label, 
            obj.subject._meta.model_name, 
            obj.subject.pk, 
            obj.subject.name,
        )

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'date',
        'balance_link',
        'title',
        'value',
    )
    def balance_link(self, obj):
        return format_html('<a href="/admin/{}/{}/{}/change/">{}</a>', 
            obj.balance._meta.app_label, 
            obj.balance._meta.model_name, 
            obj.balance.pk, 
            obj.balance.user.username,
        )