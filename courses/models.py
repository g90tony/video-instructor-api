from django.conf import settings
from django.db import models
from cloudinary.models import CloudinaryField
from django.db.models.fields.related import ForeignKey


# Create your models here.
class Profile(models.Model):
    avatar = models.CharField(max_length=255, blank=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user = models.IntegerField(null=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def create_profile(self):
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, default=None)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=255, default=None)
    description = models.TextField(default=None)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    thumbnail = CloudinaryField('image', default='yhswwpam97nojmgryvcm')
    created = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    def add_course(self):
        self.save()


class Lesson(models.Model):
    title = models.CharField(max_length=255, default=None)
    descripion = models.TextField(default=None)
    lesson = models.CharField(max_length=255, default=None)
    course = ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def add_lesson(self):
        self.save()


class RegisteredCourses(models.Model):
    profile = models.IntegerField(null=False)
    course = models.IntegerField(null=False)
    progress = models.IntegerField(default=0)

    def register_course(self):
        self.save()

        course_lessons = Lesson.objects.filter(course=self.course).all()

        for lesson in course_lessons:
            initialized_progress = Progress(
                profile=self.profile, course=self.course, lesson=lesson)
            initialized_progress.init_progress()


class Progress(models.Model):
    profile = models.IntegerField(null=False)
    course = models.IntegerField(null=False)
    lesson = models.IntegerField(null=False)
    is_complete = models.BooleanField(default=False)

    def init_progress(self):
        self.save()

    def mark_complete(self):
        self.is_complete = True
        self.save()
