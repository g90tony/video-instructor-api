import cloudinary.uploader
from django.http import response

from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

from .models import Category, Course, Lesson, Profile, Progress, RegisteredCourses
from .serializers import CourseSerializer, LessonSerializer, ListCourseSerializer, ListLessonSerializer, ProfileSerializer, ProgressSerializer, RegisterCourseSerializer, ListProfileSerializer, ListCategorySerializer, ListProgressSerializer, ListRegisterCourseSerializer, UserSerializer
from django.contrib.auth import get_user_model
User = get_user_model()

# ===========================================================================================================================================================================================================================================================================================================
# API Routes
# ===========================================================================================================================================================================================================================================================================================================

# //////////////////////////////////////////////////////////////////////////////////////////////////////
# API Routes
# Name: ListUser
# Endpoint: api/categories/
# Desc: handles all category creation requests
# Methods: GET


class SingleUser(APIView):
    permission_classes = [IsAuthenticated]

    def get_user_instance(self, pk):
        try:
            user_instance = User.objects.get(id=pk)
            return user_instance

        except User.DoesNotExist:
            raise response.Http404

    def post(self, request, format=None):

        serializer = UserSerializer(
            request.data, context={'request': request}, many=True)

        if serializer.is_valid():
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        else:
            return response(status=status.HTTP_400_BAD_REQUEST)

# //////////////////////////////////////////////////////////////////////////////////////////////////////
# API Routes
# Name: ListUser
# Endpoint: api/categories/
# Desc: handles all category creation requests
# Methods: GET


class ListUsers(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):

        serializer = UserSerializer(
            request.data, context={'request': request}, many=True)

        if serializer.is_valid():
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        else:
            return response(status=status.HTTP_400_BAD_REQUEST)


# //////////////////////////////////////////////////////////////////////////////////////////////////////
# API Routes
# Name: ListCategory
# Endpoint: api/categories/
# Desc: handles all category creation requests
# Methods: GET


class ListCategory(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        all_categories = Category.objects.all()

        serializer = ListCategorySerializer(
            all_categories, context={'request': request}, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


# /////////////////////////////////////////////////////////////////////////////////////////////////////
# API Routes
# Name: SingleCourse
# Endpoint: api/browse/courses/<course_id>
# Desc: handles all single course requests
# Methods: GET
class SingleCourse(APIView):
    permission_classes = [IsAuthenticated]

    def get_course_instance(self, pk):
        try:
            return Course.objects.get(id=pk)

        except Course.DoesNotExist:
            raise response.Http404

    def get(self, request, course_id, format=None):

        course_instance = self.get_course_instance(course_id)

        serializer = CourseSerializer(
            course_instance, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)


# //////////////////////////////////////////////////////////////////////////////////////////////////////
# API Routes
# Name: ListCourse
# Endpoint: api/courses/
# Desc: handles all bulk courses requests
# Methods: GET, POST
class ListCourses(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        all_courses = Course.objects.all()

        serializer = ListCourseSerializer(
            all_courses,  context={'request': request}, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

# //////////////////////////////////////////////////////////////////////////////////////////////////////
# API Routes
# Name: ListCourse
# Endpoint: api/courses/registered/enroll/<course_id>/<profile_id>
# Desc: handles all bulk courses requests
# Methods: GET, POST


class EnrollCourse(APIView):
    permission_classes = [IsAuthenticated]

    def create_registered_lessons(self, course_id, profile_id):
        tracked_course_lesson = dict()

        course_model_instance = Course.objects.get(id=course_id)
        course_lessons = Lesson.objects.filter(
            course=course_model_instance).values()

        for lesson in course_lessons:
            tracked_lesson_model_instance = Progress(
                lesson=lesson['id'], course=course_id, profile=profile_id)

            try:
                tracked_lesson_model_instance.save()
                print(tracked_lesson_model_instance.objects.values())
            except:
                print(f"An error occured saving"+lesson['title'])

    def post(self, request, format=None):

        serializer = ListRegisterCourseSerializer(data=request.data)

        if serializer.is_valid():
            self.create_registered_lessons(request.data.get(
                'course'), request.data.get('profile'))
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# //////////////////////////////////////////////////////////////////////////////////////////////////////
# API Routes
# Name: SimilarCourses
# Endpoint: api/courses/browse/similar/<category>
# Desc: handles all bulk courses requests
# Methods: GET, POST


class SimilarCourses(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, category, format=None):

        all_courses = Course.objects.filter(category=category)[:3]

        serializer = ListCourseSerializer(
            all_courses,  context={'request': request}, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

# //////////////////////////////////////////////////////////////////////////////////////////////////////
# API Routes
# Name: RecentCourses
# Endpoint: api/courses/browse/recent/
# Desc: handles all bulk courses requests
# Methods: GET, POST


class RecentCourses(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        all_courses = Course.objects.all()[:6]

        serializer = ListCourseSerializer(
            all_courses,  context={'request': request}, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


# //////////////////////////////////////////////////////////////////////////////////////////////////////
# API Routes
# Name: List Course Lessons
# Endpoint: api/courses/
# Desc: handles all bulk courses requests
# Methods: GET, POST
class ListRegisterLessons(APIView):
    permission_classes = [IsAuthenticated]

    def get_course_lessons(self, profile_id, course_id):

        registered_lessons = list()
        try:
            course_model_instance = Course.objects.get(id=course_id)

            course_lessons = Lesson.objects.filter(
                course=course_model_instance).all()

            for lesson in course_lessons:
                registered_lesson = {}
                lessonObj = lesson
                lesson_tracking = Progress.objects.filter(
                    lesson=lessonObj.id, course=course_id, profile=profile_id).first()

                registered_lesson['id'] = lessonObj.id
                registered_lesson['title'] = lessonObj.title
                registered_lesson['descripion'] = lessonObj.descripion
                registered_lesson['lesson'] = lessonObj.lesson
                registered_lesson['course'] = lessonObj.id
                registered_lesson['is_complete'] = lesson_tracking.is_complete

                registered_lessons.append(registered_lesson)
                print(registered_lesson)

            return registered_lessons

        except Course.DoesNotExist:
            raise response.Http404

    def get(self, request, profile_id, course_id, format=None):

        course_lessons = self.get_course_lessons(profile_id, course_id)

        return Response(data=course_lessons, status=status.HTTP_200_OK)


# //////////////////////////////////////////////////////////////////////////////////////////////////////
# API Routes
# Name: ListRegisterCourse
# Endpoint: api/courses/registered
# Desc: handles all bulk registed courses requests
# Methods: GET, POST

class ListRegisterCourse(APIView):
    permission_classes = [IsAuthenticated]

    def get_registered_courses(self, pk):
        try:
            registered_courses_list = RegisteredCourses.objects.filter(
                profile=pk).values()

            return registered_courses_list

        except Profile.DoesNotExist:
            raise response.Http404

    def get_registered_course(self, pk):
        course_instance = Course.objects.filter(id=pk).values()[0]
        course_model_instance = Course.objects.filter(id=pk).first()
        category_instance = Category.objects.filter(
            id=course_instance['category_id']).values()[0]

        edited_instance = dict()

        edited_instance['id'] = course_instance['id']
        edited_instance['name'] = course_instance['name']
        edited_instance['description'] = course_instance['description']
        edited_instance['category_id'] = course_instance['category_id']
        edited_instance['created'] = course_instance['created']
        edited_instance['category'] = category_instance
        edited_instance['thumbnail'] = course_model_instance.thumbnail.url

        return edited_instance

    def get(self, request, profile_id, format=None):
        _registeredCourses = list()
        _registeredCourses = self.get_registered_courses(profile_id)
        _registeredCourse = dict()
        all_registered_courses = list()

        for course in _registeredCourses:
            _registeredCourse = self.get_registered_course(course['course'])
            _registeredCourse['progress'] = course['progress']

            print(_registeredCourse)

            all_registered_courses.append(_registeredCourse)

            # course_response["progress"] = registeredCourses.progress

        return Response(data=all_registered_courses, status=status.HTTP_200_OK)


# /////////////////////////////////////////////////////////////////////////////////////////////////////
# API Routes
# Name: SingleCourse
# Endpoint: api/browse/courses/<course_id>
# Desc: handles all single course requests
# Methods: GET
class SingleRegisteredCourse(APIView):
    permission_classes = [IsAuthenticated]

    def get_registered_course_instance(self, profile_id, course_id):
        try:
            registered_join = RegisteredCourses.objects.filter(
                profile=profile_id, course=course_id).values()[0]

            course_instance = Course.objects.filter(
                id=registered_join['course']).values()[0]

            course_model_instance = Course.objects.filter(id=course_id).first()

            category_instance = Category.objects.filter(
                id=course_instance['category_id']).values()[0]

            edited_instance = dict()

            edited_instance['id'] = course_instance['id']
            edited_instance['name'] = course_instance['name']
            edited_instance['description'] = course_instance['description']
            edited_instance['category_id'] = course_instance['category_id']
            edited_instance['created'] = course_instance['created']
            edited_instance['category'] = category_instance
            edited_instance['thumbnail'] = course_model_instance.thumbnail.url
            edited_instance['progress'] = registered_join['progress']

            return edited_instance

        except RegisteredCourses.DoesNotExist:
            raise response.Http404

    def get(self, request, profile_id, course_id, format=None):

        registered_course_instance = self.get_registered_course_instance(
            profile_id, course_id)

        print(registered_course_instance)

        return Response(data=registered_course_instance, status=status.HTTP_200_OK)


# //////////////////////////////////////////////////////////////////////////////////////////////////////
# API Routes
# Name: SearchAllCourses
# Endpoint: api/courses/browse/search/
# Data: search_query: string
# Desc: handles all bulk courses requests
# Methods: POST
class SearchAllCourses(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        print(request)
        search_query = request.data['search_query']
        search_results = list()

        print(search_query)
        all_courses = Course.objects.all()

        for course in all_courses:
            if search_query in course.name:
                search_results.append(course)

        serializer = ListCourseSerializer(search_results, context={
            'request': request}, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

# //////////////////////////////////////////////////////////////////////////////////////////////////////
# API Routes
# Name: SearchRegisteredCourses
# Endpoint: api/courses/registered/search/
# Data: search_query: string
# Desc: handles all bulk courses requests
# Methods: POST


class SearchRegisteredCourses(APIView):
    permission_classes = [IsAuthenticated]

    def get_required_instances(self, pk):
        profile_instance = Profile.objects.get(id=pk)

        return profile_instance

    def post(self, request, profile_id, format=None):
        print(request)
        search_query = request.data['search_query']
        search_results = list()

        print(search_query)
        profile_instance = self.get_required_instances(profile_id)
        registered_courses = RegisteredCourses.objects.all(
            profile=profile_instance)

        for course in registered_courses:
            if search_query in course.name:
                search_results.append(course)

        serializer = ListRegisterCourseSerializer(search_results, context={
            'request': request}, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


# //////////////////////////////////////////////////////////////////////////////////////////////////////
# API Routes
# Name: SingleLesson
# Endpoint: api/lesson/<course_id>
# Desc: handles all single lessons requests
# Methods: GET,
class SingleCourseLessons(APIView):
    permission_classes = [IsAuthenticated]

    def get_lesson_instance(self, course_pk, lesson_pk):

        course_instance = Course.objects.get(id=course_pk)

        lesson_instance = Lesson.objects.filter(
            id=lesson_pk, course=course_instance).first()

        return lesson_instance

    def get(self, request, course_id, lesson_id, format=None):

        lesson_instance = self.get_lesson_instance(course_id, lesson_id)

        serializer = LessonSerializer(lesson_instance, context={
            'request': request})

        return Response(data=serializer.data, status=status.HTTP_200_OK)


# /////////////////////////////////////////////////
# Name: SingleProfile
# Endpoint: api/profile/<profile_id>
# Desc: handles all requests for a single profile
# Methods: GET
class SingleProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get_profile_instance(self, pk):
        try:
            return Profile.objects.get(user=pk)

        except Profile.DoesNotExist:
            raise response.Http404

    def get(self, request, user_id, format=None):
        profile_instance = self.get_profile_instance(user_id)

        serializer = ListProfileSerializer(
            profile_instance, context={"request": request}, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


# /////////////////////////////////////////////////
# Name: UpdateProfile
# Endpoint: api/profile/<profile_id>/update/avatar
# Desc: handles update requests for a single profile
# Methods: PUT


class UpdateProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get_profile_instance(self, pk):
        try:
            return Profile.objects.get(id=pk)
        except Profile.DoesNotExist:
            raise response.Http404

    def put(self, request, profile_id, format=None):
        profile_instance = self.get_profile_instance(profile_id)

        serializer = ListProfileSerializer(
            profile_instance, context={"request": request}, many=False)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


# /////////////////////////////////////////////////
# Name: ListProfile
# Endpoint: api/profile/
# Desc: handles all requests for a single profile
# Methods:POST
class ListProfile(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_user_profile_instance(self, pk):
        try:
            return User.objects.get(id=pk)

        except User.DoesNotExist:
            raise response.Http404

    def get(self, request, format=None):

        all_profiles = Profile.objects.all()

        serializer = ListProfileSerializer(
            all_profiles, context={'request': request}, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):

        file = request.data.get('picture')

        user_id = request.data.get('user')

        upload_data = cloudinary.uploader.upload(file)

        new_profile = {
            "avatar": upload_data['url'],
            "first_name": request.data.get('first_name'),
            "last_name": request.data.get('last_name'),
            "user": user_id,
        }

        serializer = ListProfileSerializer(
            data=new_profile, context=({'request': request}), many=False)

        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(data=serializer.errors)


# /////////////////////////////////////////////////////////////////////////////////////////////////////
# API Routes
# Name: SingleProgress
# Endpoint: api/progress/<progress_id>
# Desc: handles all single progress requests
# Methods: GET, POST
class SingleProgress(APIView):
    permission_classes = [IsAuthenticated]

    def get_progress_instance(self, pk):
        try:
            return Progress.objects.get(id=pk)

        except Progress.DoesNotExist:
            raise response.Http404

    def get(self, request, progress_id, format):

        progress_instance = self.get_progress(progress_id)

        serializer = ProgressSerializer(
            progress_instance, context={'request': request}, many=False)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


# //////////////////////////////////////////////////////////////////////////////////////////////////////
# API Routes
# Name: ListProgress
# Endpoint: api/progress/<course_id>+<profile_id>
# Desc: handles all bulk progress requests
# Methods: GET, POST
class ListProgress(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id, profile_id, format=None):

        all_course_progress = Progress.objects.filter(
            course=course_id, profile=profile_id).all()

        serializer = ListProgressSerializer(all_course_progress, context={
                                            'request': request}, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

# //////////////////////////////////////////////////////////////////////////////////////////////////////
# API Routes
# Name: UpdateProgress
# Endpoint: api/progress/<course_id>+<profile_id>
# Desc: handles all bulk progress requests
# Methods: POST


class CurrentProgress(APIView):
    permission_classes = [IsAuthenticated]

    def get_progress_instance(self, course_pk, profile_pk):

        tracked_lesson = dict()

        progress_instance = Progress.objects.filter(
            profile=profile_pk, course=course_pk, is_complete=False).first()

        course_lesson = Lesson.objects.filter(
            id=progress_instance.lesson).first()

        if course_lesson:
            tracked_lesson['title'] = course_lesson.title
            tracked_lesson['descripion'] = course_lesson.descripion
            tracked_lesson['lesson'] = course_lesson.lesson
            tracked_lesson['course'] = course_lesson.course.id

        return tracked_lesson

    def get(self, request, course_id, profile_id, format=None):

        current_progress_instance = self.get_progress_instance(
            course_id, profile_id)

        return Response(data=current_progress_instance, status=status.HTTP_200_OK)

    def post(self, request, course_id, profile_id, format=None):

        current_progress_instance = self.get_progress_instance(
            course_id, profile_id)

        current_progress_instance.is_complete = True

        serializer = ProgressSerializer(current_progress_instance, many=False)

        if serializers.is_valid():
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UploadView(APIView):
    parser_classes = (
        MultiPartParser,
        JSONParser,
    )

    @staticmethod
    def post(request):
        file = request.data.get('picture')

        upload_data = cloudinary.uploader.upload(file)
        return Response({
            'status': 'success',
            'data': upload_data,
        }, status=201)
