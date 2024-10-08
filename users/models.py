import re
import uuid
from django.db import models
from academics.models import Course
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

class UserManager(BaseUserManager):
    """
    Custom user manager to handle user creation logic for superuser, teacher, and student.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field is required'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self.create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email):
        return self.get(email=email)
    
    def create_teacher(self, staff_number, password=None):
        staff_number_format = r'TC-NIT-(CCT|HSS)-(201[2-9]|20[0-3][0-4])-([0-9]{3})$'
        if not staff_number:
            raise ValueError(_('Staff number field is required'))
        if not password:
            raise ValueError(_('Password field is required'))
        if not re.match(staff_number_format, staff_number):
            raise ValueError(_('Invalid staff number format'))

        teacher = self.model(staff_number=staff_number, is_teacher=True)
        teacher.set_password(password)
        teacher.save(using=self._db)
        return teacher
    
    def create_student(self, registration_number, password=None):
        registration_number_format = r'^NIT/(BIT|BCS|BMPR)/(201[5-9]|20[2-3][0-4])/([0-9]{4})$'
        registration_number_match = re.match(registration_number_format, registration_number)
        
        if not registration_number:
            raise ValueError(_('Registration number is required'))
        if not password:
            raise ValueError(_('Password is required'))
        if not registration_number_match:
            raise ValueError(_('Incorrect Registration number format'))
        
        course_identifier = registration_number_match.group(1)
        COURSE_MAP = {
            'BIT': 'Information Technology',
            'BMPR': 'Marketing and Public Relations',
            'BCS': 'Computer Science',
        }
        course_name = COURSE_MAP.get(course_identifier)
        if not course_name:
            raise ValueError(_('Course for registration number not found'))

        try:
            course = Course.objects.get(name=course_name)
        except ObjectDoesNotExist:
            raise ValueError(_('Course not found in the system'))

        student = self.model(registration_number=registration_number, is_student=True)
        student.set_password(password)
        student.save(using=self._db)

        course.students.add(student)
        return student

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True)
    registration_number = models.CharField(max_length=120, blank=True, null=True)
    staff_number = models.CharField(max_length=120, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
