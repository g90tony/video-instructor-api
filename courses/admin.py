from django.contrib import admin

from .models import Category, Course, Lesson, Profile, Progress, RegisteredCourses
# Register your models here.
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Profile)
admin.site.register(Progress)
admin.site.register(RegisteredCourses)