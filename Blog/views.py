from django.shortcuts import get_object_or_404
from .models import Post,Comment
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PostSerializer,CommentSerializer,PostViewSerializer
from rest_framework import status,generics
from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from users.models import CustomUser
from users.serializers import UserSerializer
import logging

logger = logging.getLogger(__name__)

class PostPagination(PageNumberPagination):
    page_size = 5000
    page_size_query_param = 'page_size'
    max_page_size = 100
    def get_paginated_response(self, data):
        return Response({
            "error": False,
            "message": "Posts fetched successfully",
            "pagination": {
                "current_page": self.page.number,
                "total_pages": self.page.paginator.num_pages,
                "total_posts": self.page.paginator.count,
                "has_next": self.page.has_next(),
                "has_previous": self.page.has_previous(),
                "next": self.get_next_link(),  
                "previous": self.get_previous_link() 
            },
            "data": data
        })


class PostListView(ListAPIView):
    queryset = Post.objects.filter(status=Post.Status.PUBLISHED,post_type=Post.GENERAL)
    serializer_class = PostSerializer
    pagination_class = PostPagination
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.get_queryset())
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            "error": False,
            "message": "Posts fetched successfully",
            "data": serializer.data
        })


class PostDetailView(RetrieveAPIView):
    queryset = Post.objects.filter(status=Post.Status.PUBLISHED)
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
      
            pk = int(self.kwargs['pk'])
            post = get_object_or_404(self.queryset, pk=pk)

            post_data = self.serializer_class(post).data

            return Response({
                "error": False,
                "message": "Post fetched successfully",
                "data": post_data
            })
        
        except ValueError:
            # Return an error response if the 'pk' is invalid
            raise ValidationError({"error": "Invalid ID format"})


class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        # registration_number = self.kwargs['registration_number']
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        count = queryset.count()

        return Response({
            'error' : False,
            'count': count,
            'comments': serializer.data
        })

class AuthorPostsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, author_email):
        course = request.query_params.get('course')  
        total_post_count = Post.objects.filter(author__email=author_email,status=Post.Status.PUBLISHED).count()
        published_posts = Post.objects.filter(author__email=author_email, status=Post.Status.PUBLISHED, course=course)
        serializer = PostSerializer(published_posts, many=True)
        return Response({
            'error': 'False',
            'message': 'Posts fetched successfully',
            'count': total_post_count,  
            'data': serializer.data 
        }, status=status.HTTP_200_OK)


class CourseSpecificPostsView(APIView):
    def get(self, request,course_id):
        post = Post.objects.filter(course=course_id)
        serializer = PostSerializer(post,many=True)
        return Response({
            'error' : False,
            'message' : 'Posts fetched successfully',
            'data' : serializer.data
        },status=status.HTTP_200_OK)

                
class PostCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
        serializer = CommentSerializer(data=request.data)
        
        if serializer.is_valid():
            # Save the comment with the associated post and user
            serializer.save(post=post, user=request.user)
            return Response({
                "error": "False",
                "message": "Comment uploaded",
                "data": serializer.data,
                "status": status.HTTP_201_CREATED
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class CreatePost(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Post Created Successfully"}, status=status.HTTP_201_CREATED)
  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class DeleteAllPosts(APIView):
    permission_classes = [IsAuthenticated, AllowAny]  # Optional: if you want to restrict access

    def delete(self, request, format=None):
        Post.objects.all().delete()
        return Response({"message": "All posts have been deleted."}, status=status.HTTP_204_NO_CONTENT)
    
class DeletePostByID(APIView):

    permission_classes = [AllowAny]
    def delete(self,request, id, format= None):
        Post.objects.get(id = id).delete()
        return Response({"message":"Post deleted successfully"}, status=status.HTTP_202_ACCEPTED)
    
                
class RecordPostView(APIView):
    def post(self, request, post_id, registration_number):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        user = request.user if request.user.is_authenticated else None
        serializer = PostViewSerializer(data={
            'post': post.id,
            'user': user.id if user else None,
            'registration_number': registration_number
        })

        if serializer.is_valid():
            serializer.save()
            post.views_count += 1
            post.save()
            return Response({
                "message": "Views recorded successfully",
                "data": {
                    "post": post.id,
                    "user": user.id if user else None  
                }
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
#The search logic for custom User class had to be implemented in this app  for the purpose of 
# creating an intelligent search engine in mobile app frontend. Feel free to write separate logics
# in each app 

class SearchView(generics.ListAPIView):
    
    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        search_type = self.request.query_params.get('search_type', 'post')

        if not query:
            return []

        if search_type == 'teacher':
            return CustomUser.objects.filter(
                Q(is_teacher=True) & 
                (Q(email__icontains=query) | Q(registration_number__icontains=query))
            )
        else:
            return Post.objects.filter(
                Q(title__icontains=query) | Q(body__icontains=query)
            )
    
    def list(self, request, *args, **kwargs):
        search_type = request.query_params.get('search_type', 'post')
        queryset = self.get_queryset()

        if not request.query_params.get('q', ''):
            return Response({
                'error': 'true',
                'message': 'No search data'
            }, status=status.HTTP_400_BAD_REQUEST)

        count = queryset.count()

        if search_type == 'teacher':
            serializer = UserSerializer(queryset, many=True)
        else:
            serializer = PostSerializer(queryset, many=True)

        return Response({
            'error': 'False',
            'message': 'Query Success',
            'count': count,
            'data': serializer.data
        }, status=status.HTTP_200_OK)