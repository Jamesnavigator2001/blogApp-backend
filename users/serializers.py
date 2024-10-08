
from rest_framework import serializers
from academics.serializers import CourseSerializer
from users.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)  # Ensure this matches the related_name   
    class Meta:
        model = CustomUser
        fields = ['email', 'staff_number', 'password', 'registration_number', 'is_student', 'is_teacher', 'courses']
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        password = validated_data.pop('password')
        registration_number = validated_data.get('registration_number')
        
        is_student = validated_data.get('is_student', False)
        is_teacher = validated_data.get('is_teacher', False)
        is_staff = validated_data.get('is_staff', False)

        if is_student:
            user = CustomUser.objects.create_student(registration_number=registration_number, password=password)
        else:
            # For teachers, admins, and other users
            user = CustomUser(**validated_data)
            if password:
                user.set_password(password)  # Hash the password
            user.save()

        # Set additional fields like email and staff_number if present
        user.email = validated_data.get('email', '')
        user.staff_number = validated_data.get('staff_number', '')
        user.save()

        return user
