from rest_framework import serializers
from users.models import CustomUser
from .models import Post, Comment , PostView
from academics.models import Department, Course

class PostSerializer(serializers.ModelSerializer):
    author_email = serializers.EmailField(write_only=True)  
    author_username = serializers.SlugRelatedField(
    source='author',
    slug_field='email',
    read_only=True
    )

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'post_type' ,'course','file_upload' ,'file_name', 'image', 'status', 'author_email' , 'views_count', 'author_username','publish']
        read_only_fields = ['author' , 'author_email']  

    def validate(self, data):
        
        file = data.get('file_upload' , None)
        file_name = data.get('file_name' , None)

        if file and file.name.endswith('.pdf') and not file_name:
            raise serializers.ValidationError('Please provide a meaningful name for the file')
        
        return data

    
    def create(self, validated_data):
        author_email = validated_data.pop('author_email')
        try:
            author = CustomUser.objects.get(email=author_email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({"author_email": "Author with this email does not exist"})
        
        validated_data['author'] = author
        return Post.objects.create(**validated_data)
    


class CommentSerializer(serializers.ModelSerializer):
    registration_number = serializers.CharField(source='user.registration_number', read_only=True)
    email = serializers.CharField(source='user.email', read_only = True)

    class Meta:
        model = Comment
        fields = ['id', 'created', 'post', 'body', 'active', 'registration_number', 'email']

class PostViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostView
        fields = ['post' , 'user']

        def validate_post(self, value):
            try:
                Post.objects.get(id=value.id)
            except Post.DoesNotExist:
                raise serializers.ValidationError("Post not found")
            
            return value
        

