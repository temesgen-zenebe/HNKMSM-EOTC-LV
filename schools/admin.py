# admin.py
from django.contrib import admin
from .models import Course, Chapter, Resources,Quiz, Question, Answer, Result, Report,Progress,QuationsAndAnswer

admin.site.register(Course)
admin.site.register(Chapter)
admin.site.register(Resources)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Result)
admin.site.register(Report)
admin.site.register(Progress)
class QuationsAndAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'viewed_by', 'is_answered' ,'question', 'answer')  # Add 'is_answered' to the list display

    def is_answered(self, obj):
        return obj.answer is not None
    is_answered.boolean = True  # Displays a nice True/False icon instead of "True"/"False"
    is_answered.short_description = 'Answered'  # Custom column header name
admin.site.register(QuationsAndAnswer, QuationsAndAnswerAdmin)
