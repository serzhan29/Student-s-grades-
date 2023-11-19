from django.contrib import admin
from .models import Student,Course, Fakulty, Subject, Group, \
    SRStwo, SRSone, FinalResult, Teacher, TeacherGroup


class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "surname", "name", "url", "group", "gpa",)
    list_display_links = ("surname", "name", )
    search_fields = ("surname", "name", )
admin.site.register(Student, StudentAdmin)


class SRS_ONE(admin.ModelAdmin):
    list_display = ("id", "student", "subject", "week1", "week2", "week3", "week4", "week5", "week6", "week7", "SRS_1", )
    list_display_links = ("id", "student", "subject", )
    search_fields = ("id","student", "subject")
    #list_filter = ['student', 'subject']

admin.site.register(SRSone, SRS_ONE)


class SRS_TYO(admin.ModelAdmin):
    list_display = ("id", "student", "subject", "week8", "week9", "week10",  "week11",  "week12",  "week13",  "week14", "week15", "SRS_2", )
    list_display_links = ("id", "student", "subject", )
    search_fields = ['id', 'student', 'subject']
    #list_filter = ['student', 'subject']

admin.site.register(SRStwo, SRS_TYO)


class FINAL(admin.ModelAdmin):
    list_display = ("id", "student", "subject", "exam_grade" , "final_result2", )
    list_display_links = ("id", "student" , "subject", )
    search_fields = ['id', 'student', 'subject']
    #list_filter = ['student', 'subject']


admin.site.register(FinalResult, FINAL)

admin.site.register(Course)


class FAKULTY(admin.ModelAdmin):
    list_display = ("id", "name", "code", )
    list_display_links = ("id", "name", )

admin.site.register(Fakulty, FAKULTY)


class TEACHER(admin.ModelAdmin):
    list_display = ("id", "name", "surname",)
    list_display_links = ("id", "name", "surname",)

admin.site.register(Teacher, TEACHER)

admin.site.register(Subject)
admin.site.register(Group)
admin.site.register(TeacherGroup)
