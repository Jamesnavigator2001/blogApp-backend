from django.db import models
import uuid

class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    department_name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'DEPARTMENT'
        verbose_name_plural = 'DEPARTMENTS'

    def __str__(self):
        return self.department_name
    

class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=100, unique=True)
    students = models.ManyToManyField(
        'users.CustomUser', 
        related_name='courses',
        limit_choices_to={'is_student': True}
    )
    # teachers = models.ManyToManyField(
    #     'users.CustomUser', 
    #     related_name='taught_courses', 
    #     limit_choices_to={'is_teacher': True}
    # )

    def __str__(self):
        return self.name
    
