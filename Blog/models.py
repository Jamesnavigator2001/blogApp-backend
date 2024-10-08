import uuid
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.urls import reverse
from users.models import CustomUser
from academics.models import Course


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    class Status(models.TextChoices):
        DRAFT = 'DF', 'DRAFT'
        PUBLISHED = 'PB', 'PUBLISHED'

    GENERAL = 'G'
    COURSE_SPECIFIC = 'C'
    POST_TYPE_CHOICES = [
        (GENERAL , 'General'), 
        (COURSE_SPECIFIC, 'Course Specific'),
    ]

    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, blank=True)
    body = models.TextField()
    post_type = models.CharField(max_length=1, choices=POST_TYPE_CHOICES, default=GENERAL)
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.SET_NULL, related_name='posts')
    file_upload = models.FileField(upload_to='uploads/', blank=True, null=True)
    file_name = models.CharField(max_length=120)
    image = models.ImageField(null=True, blank=True, upload_to='media/')
    publish = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blog_posts')
    views_count = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['publish', 'created'])]
        verbose_name = 'POST'
        verbose_name_plural = 'POSTS'

    def clean(self):
        if not self.author.is_teacher:
            raise ValidationError("The author must be a teacher.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail_view', args=[str(self.id)])
    
    def is_visible_to(self, user):
        if self.post_type == Post.GENERAL:
            return True
        elif self.post_type == Post.COURSE_SPECIFIC and user.is_student:
            return self.course in user.courses.all()
        return False


class PostView(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['created'])]
        verbose_name = 'COMMENT'
        verbose_name_plural = 'COMMENTS'

    def __str__(self):
        return f"Comment by {self.user.registration_number} on {self.post}"
