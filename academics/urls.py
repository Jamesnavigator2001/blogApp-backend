from django.urls import path
from .views import CourseView,CreateCourse


urlpatterns = [

    #courses
    path('api/courses/',CourseView.as_view(),name='all_courses'),
    # path('api/courses/<id>/', CourseView.as_view()),
    path('api/courses/create/', CreateCourse.as_view(), name='create_course')
]