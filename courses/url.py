"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from . import views as API_ROUTES

urlpatterns = [
    path('categories/', API_ROUTES.ListCategory.as_view()),

    path('courses/browse/', API_ROUTES.ListCourses.as_view()),
    path('courses/browse/search/', API_ROUTES.SearchAllCourses.as_view()),
    path('courses/browse/<int:course_id>', API_ROUTES.SingleCourse.as_view()),
    path('courses/browse/similar/<int:category>',
         API_ROUTES.SimilarCourses.as_view()),
    path('courses/browse/recent',
         API_ROUTES.RecentCourses.as_view()),

    path('courses/registered/', API_ROUTES.ListCourses.as_view()),
    path('courses/registered/enroll/',
         API_ROUTES.EnrollCourse.as_view()),
    path('courses/registered/search/',
         API_ROUTES.SearchRegisteredCourses.as_view()),
    path('courses/registered/<int:profile_id>',
         API_ROUTES.ListRegisterCourse.as_view()),
    path('courses/registered/<int:course_id>/<int:profile_id>',
         API_ROUTES.SingleRegisteredCourse.as_view()),
    path('courses/registered/<int:course_id>/<profile_id>/lessons',
         API_ROUTES.ListRegisterLessons.as_view()),
    path('courses/registered/<int:course_id>/<profile_id>/lesson/<int:lesson_id>',
         API_ROUTES.SingleCourseLessons.as_view()),

    path('profile/<int:user_id>', API_ROUTES.SingleProfile.as_view()),
    path('profile/create', API_ROUTES.ListProfile.as_view()),
    path('profile/<int:profile>/update/avatar',
         API_ROUTES.UpdateProfile.as_view()),

    path('progress/courses/<int:course_id>/<int:profile_id>',
         API_ROUTES.ListProgress.as_view()),
    path('progress/current/<int:course_id>/<int:profile_id>',
         API_ROUTES.CurrentProgress.as_view()),

    path('image/uploader',
         API_ROUTES.UploadView.as_view()),

]
