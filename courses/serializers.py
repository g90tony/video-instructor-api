from django.conf import settings
from django.db import models
from django.db.models import fields
from rest_framework import serializers

from .models import Category, Course, Lesson, Profile, Progress, RegisteredCourses
from users.serializers import UserSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class CourseSerializer(serializers.ModelSerializer):

    thumbnail = serializers.SerializerMethodField()
    category = CategorySerializer(many=False)

    class Meta:
        model = Course
        fields = ("id", "name", "description", "category", "thumbnail",)

    def get_thumbnail(self, course):
        request = self.context.get('request')
        thumbnail = course.thumbnail.url

        return request.build_absolute_uri(thumbnail)


class LessonSerializer(serializers.ModelSerializer):

    course = CourseSerializer(many=False)

    class Meta:
        model = Lesson
        fields = ("id", "title", "descripion", "lesson", "course",)


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ("id", "avatar", "first_name", "last_name", "user")


class ProgressSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)
    course = CourseSerializer(many=False)
    lesson = LessonSerializer(many=False)

    class Meta:
        model = Progress
        fields = ("id", "profile", "course", "lesson",)


class RegisterCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model: RegisteredCourses
        fields = ("profile", "course", "progress",)


# List Models Serializers
class ListCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ListCourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_thumbnail(self, course):
        request = self.context.get('request')
        thumbnail = course.thumbnail.url

        return request.build_absolute_uri(thumbnail)


class ListLessonSerializer(serializers.ModelSerializer):

    course = CourseSerializer(many=False)

    class Meta:
        model = Lesson
        fields = '__all__'


class ListProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'


class ListProgressSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)
    course = CourseSerializer(many=False)
    lesson = LessonSerializer(many=False)

    class Meta:
        model = Progress
        fields = '__all__'


class ListRegisterCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = RegisteredCourses
        fields = '__all__'
