from django.contrib import admin
from .models import Post, Comment
from academics.models import Department
from users.models import CustomUser
from django.contrib.auth.admin import UserAdmin

# Register your models here.
models = [Post,Department,]


@admin.register(Post)
class AdminPage(admin.ModelAdmin):
    list_display = ['title' , 'status', 'publish' ,'author' , 'created' , 'modified']
    search_fields = ['title' , 'publish' , 'status' , 'created']
    list_filter = ['publish']
    prepopulated_fields = {"slug" : ('title' , )}
    
class CommentSection(admin.ModelAdmin):
    list_display = ('get_registration_number', 'post', 'body', 'created', 'active')
    
    def get_registration_number(self, obj):
        return obj.user.registration_number
    
    get_registration_number.short_description = 'Registration Number'


@admin.register(Department)
class Departments(admin.ModelAdmin):
    list_display = ['department_name' , 'description']
    search_fields = ['department_name' , 'description']

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_student', 'is_teacher')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_student', 'is_teacher'),
        }),
    )
    list_display = ('email', 'is_student', 'is_teacher', 'is_staff', 'is_superuser')
    search_fields = ('email', 'registration_number', 'staff_number')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
