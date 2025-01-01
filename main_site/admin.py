from django.contrib import admin
from .models import *
from django.utils.html import format_html
# Register your models here.

# ! User:
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'username', 
        'password',
        'balance',
        )
    search_fields = (
        'username',
        )
    list_filter = (
        'username',
        )

# ! UserInfo:
@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'user_link',
        'name',
        'email',
        'address',
        'phoneNumber',
        'dob',
        'school',
    )

    def user_link(self, obj):
        return format_html('<a href="/admin/{}/{}/{}/change/">{}</a>', 
            obj.user._meta.app_label, 
            obj.user._meta.model_name, 
            obj.user.pk, 
            obj.user.username,
        )    
    user_link.short_description = 'Account'

    
# ! Term
@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'startDate',
        'endDate',
        'totalOfMonths',
        'userLink',
    )

    def userLink(self, obj):
        user_info = UserInfo.objects.filter(user = obj.user).first()
        return format_html('<a href="/admin/{}/{}/{}/change/">{}</a>', 
            user_info._meta.app_label, 
            user_info._meta.model_name, 
            user_info.pk, 
            user_info.name,
        )    
    userLink.short_description = 'User'  
    

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'startDate',
        'endDate',
        'status',
        'termLink',
    )
    def termLink(self, obj):
        return format_html('<a href="/admin/{}/{}/{}/change/">{}</a>', 
            obj.term._meta.app_label, 
            obj.term._meta.model_name, 
            obj.term.pk, 
            obj.term.name,
        )
    termLink.short_description = 'Term'
    
    
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'classLink',
    )
    def classLink(self, obj):
        return format_html('<a href="/admin/{}/{}/{}/change/">{}</a>', 
            obj.class_object._meta.app_label, 
            obj.class_object._meta.model_name, 
            obj.class_object.pk, 
            obj.class_object.name,
        )
    classLink.short_description = 'Class'
    
@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'startTime',
        'endTime',
        'userLink',
        'status',
    )
    def userLink(self, obj):
        if obj.user:
            return format_html(
                '<a href="/admin/{}/{}/{}/change/">{}</a>', 
                obj.user._meta.app_label, 
                obj.user._meta.model_name, 
                obj.user.pk, 
                obj.user.username,
            )
        else:
            return "No user"
    userLink.short_description = 'User'

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'startTime',
        'endTime',
        'type',
        'note',
        # Link fields
        'shiftLink',
        'classLink',
        'subjectLink',
        'chaptersLink',
    )
    def chaptersLink(self, obj):
        chapters = obj.chapter.all()
        if not chapters:
            return "No Chapters"
        res = ''
        for chapter in chapters:
            res += f'<a href="/admin/{chapter._meta.app_label}/{chapter._meta.model_name}/{chapter.pk}/change/">Chương {chapter.number}. {chapter.title}</a><br>'
        return format_html(
            res
        )
    chaptersLink.short_description = 'Chapters'

    def subjectLink(self, obj):
        if obj.subject:
            return format_html('<a href="/admin/{}/{}/{}/change/">{}</a>', 
                obj.subject._meta.app_label, 
                obj.subject._meta.model_name, 
                obj.subject.pk, 
                obj.subject.name,
            )
        else:
            return "No subject"
    subjectLink.short_description = 'Subject'

    def shiftLink(self, obj):
        if obj.shift:
            return format_html('<a href="/admin/{}/{}/{}/change/">{}</a>', 
                obj.shift._meta.app_label, 
                obj.shift._meta.model_name, 
                obj.shift.pk, 
                obj.shift.name,
            )
        else:
            return "No shift"
    shiftLink.short_description = 'Shift'

    def classLink(self, obj):
        if obj.classObj:
            return format_html('<a href="/admin/{}/{}/{}/change/">{}</a>', 
                obj.classObj._meta.app_label, 
                obj.classObj._meta.model_name, 
                obj.classObj.pk, 
                obj.classObj.name,
            )
        else:
            return "No class"
    classLink.short_description = 'Class'
    
# ! Course:
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'teacher',
        'subjectLink',
        'linkClick',
    )

    def subjectLink(self, obj):
        return format_html('<a href="/admin/{}/{}/{}/change/">{}</a>', 
            obj.subject._meta.app_label, 
            obj.subject._meta.model_name, 
            obj.subject.pk, 
            obj.subject.name,
        )
    subjectLink.short_description = 'Subject'

    def linkClick(self,obj):
        return format_html('<a href="{}">LINK</a>',obj.link)
    linkClick.short_description = 'URL'

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'NAT',
        'subjectLink',
        'linkClick',
    )

    def NAT(self, obj):
        return f'Chapter {obj.number}. {obj.title}'
    NAT.short_description = 'Title'

    def subjectLink(self, obj):
        if obj.subject:
            return format_html('<a href="/admin/{}/{}/{}/change/">{}</a>', 
                obj.subject._meta.app_label, 
                obj.subject._meta.model_name, 
                obj.subject.pk, 
                obj.subject.name,
            )
        else:
            return "No subject"
    subjectLink.short_description = 'Subject'

    def linkClick(self,obj):
        return format_html('<a href="{}">LINK</a>',obj.link)
    linkClick.short_description = 'URL'

@admin.register(ContentOfChapters)
class ContentOfChaptersAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'chapterLink',
        'title',
        'content',
        'linkClick',
    )
    def chapterLink(self, obj):
        return format_html('<a href="/admin/{}/{}/{}/change/">{}</a>', 
            obj.chapter._meta.app_label, 
            obj.chapter._meta.model_name, 
            obj.chapter.pk, 
            obj.chapter.__str__(),
        )
    def linkClick(self,obj):
        return format_html('<a href="{}">LINK</a>',obj.link)
    linkClick.short_description = 'URL'

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'linkClick',
        'file',
        'subjectLink',
    )
    def linkClick(self,obj):
        return format_html('<a href="{}">LINK</a>',obj.link)
    linkClick.short_description = 'URL'

    def subjectLink(self, obj):
        return format_html('<a href="/admin/{}/{}/{}/change/">{}</a>', 
            obj.subject._meta.app_label, 
            obj.subject._meta.model_name, 
            obj.subject.pk, 
            obj.subject.name,
        )
    subjectLink.short_description = 'Subject'

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'date',
        'userLink',
        'title',
        'type',
        'value',
    )
    def userLink(self, obj):
        if obj.user:
            return format_html('<a href="/admin/{}/{}/{}/change/">{}</a>', 
                obj.user._meta.app_label, 
                obj.user._meta.model_name, 
                obj.user.pk, 
                obj.user.username,
            )
    userLink.short_description = 'User'

@admin.register(DayPathway)
class DayPathwayAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'ordinal',
        'classLink',
    )
    def classLink(self, obj):
        return format_html('<a href="/admin/{}/{}/{}/change/">{}</a>', 
            obj.classObj._meta.app_label, 
            obj.classObj._meta.model_name, 
            obj.classObj.pk, 
            obj.classObj.name,
        )
    
@admin.register(SessionPathway)
class SessionPathwayAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'type',
        'content',
        'status',
        'iCode',
        'ordinal',
    )

@admin.register(TypeOfTransaction)
class TypeOfTransactionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'maxValue',
    )