from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from users.models import CustomUser
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserSerializer,CourseSerializer
import logging

# Create your views here.

logger = logging.getLogger(__name__)

class GetAllStudents(ListAPIView):
    queryset = CustomUser.objects.filter(is_student=True)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class GetAllTeachers(ListAPIView):

    queryset = CustomUser.objects.filter(is_teacher=True)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class RegisterTeacherView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data.copy()
        data['is_teacher'] = True  # Set teacher flag
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Teacher Registered Successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RegisterStudentView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data.copy()
        data['is_student'] = True  # Ensures that is_student is set to True
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Student Registered Successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherLoginView(APIView):
    def post(self, request):
        staff_number = request.data.get('staff_number')
        password = request.data.get('password')

        try:
            teacher = CustomUser.objects.get(staff_number=staff_number, is_teacher=True)
            if teacher.check_password(password):
                # Generate JWT tokens
                refresh = RefreshToken.for_user(teacher)
                return Response({
                    'email': teacher.email,
                    'staff_number': teacher.staff_number,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Incorrect login credentials'}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Teacher does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
class StudentLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        registration_number = request.data.get('registration_number')
        password = request.data.get('password')

        try:
            if email:
                student = CustomUser.objects.get(email=email, is_student=True)
            elif registration_number:
                student = CustomUser.objects.get(registration_number=registration_number, is_student=True)
            else:
                return Response({'error': 'Email or registration number is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Verify the password
            if student.check_password(password):
                # Generate JWT tokens
                refresh = RefreshToken.for_user(student)
                
                # Serialize the student's courses
                courses = student.courses.all()
                course_serializer = CourseSerializer(courses, many=True)
                
                return Response({
                    'error': False,
                    'message': 'Login successful',
                    'data': {
                        'email': student.email,
                        'registrationNumber': student.registration_number,
                        'courses': course_serializer.data,
                        'accessToken': str(refresh.access_token),
                        'refreshToken': str(refresh),
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': True, 'message': 'Incorrect login credentials'}, status=status.HTTP_400_BAD_REQUEST)

        except CustomUser.DoesNotExist:
            return Response({'error': True, 'message': 'Student does not exist'}, status=status.HTTP_404_NOT_FOUND)

        
class SuperAdminLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_superuser:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                })
            else:
                return Response({'error': 'You are not a super admin'}, status=403)
        else:
            return Response({'error': 'Invalid credentials'}, status=401)
        
