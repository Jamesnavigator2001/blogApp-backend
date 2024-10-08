from django.shortcuts import render
from .serializers import CourseSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Course
import logging
# Create your views here.

logger = logging.getLogger(__name__)

class CourseView(APIView):
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response({
            'error' : False,
            'message' : 'Courses Fetched Successfully',
            'data' : serializer.data
        },status=status.HTTP_200_OK)
    
        
    def get_object(self, pk):
        try:
            return Course.objects.get(id=pk)
        except Course.DoesNotExist:
            return Response({
                'error': True,
            }, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, pk):
        course = self.get_object(pk)
        serializer = CourseSerializer(course, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'error' : False,
                'message' : 'Course Changed Successfully',
                'data'  : serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request,pk):
        course = self.get_object(pk)
        course.delete()
        return Response({
            'error' : 'False',
            'message' : 'Course deleted'
        }, status=status.HTTP_204_NO_CONTENT)
    
class CreateCourse(APIView):
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'error' : 'False',
                'message' : 'Course created Successfully',
                'data' : serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
