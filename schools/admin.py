# admin.py
from django.contrib import admin
from .models import Course, Chapter, Resources,Quiz, Question, Answer, Result, Report

admin.site.register(Course)
admin.site.register(Chapter)
admin.site.register(Resources)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Result)
admin.site.register(Report)
