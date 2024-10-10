from django.urls import path,re_path
from .views import (
    PostListView, PostDetailView, CreatePost, CourseSpecificPostsView,
     AuthorPostsView, PostCommentView,
    DeleteAllPosts, DeletePostByID,CommentListView, RecordPostView, SearchView
)

urlpatterns = [

    # Post endpoints
    path('api/posts/', PostListView.as_view(), name='post_list_view'),
    path('api/posts/course-specific-posts/<str:course_id>/',CourseSpecificPostsView.as_view(), name='all-course-posts'),
    path('api/posts/create/', CreatePost.as_view(), name='create_post'),
    path('api/post/<str:pk>/', PostDetailView.as_view(), name='post_detail_view'),
    path('api/post/<str:post_id>/comment/', PostCommentView.as_view(), name='post_comment'),
    path('api/posts/<str:author_email>/', AuthorPostsView.as_view(), name='author_posts'),
    path('api/comments/<str:post_id>/', CommentListView.as_view(), name='comment_list'),
    re_path(r'^api/post/(?P<post_id>[\w\-]+)/view/(?P<registration_number>[\w\/\-]+)/$', RecordPostView.as_view(), name='record-post-view'),

    # Delete posts
    path('api/posts/delete-all/', DeleteAllPosts.as_view(), name='delete_all_posts'),
    path('api/post/delete/<str:id>/', DeletePostByID.as_view(), name='delete_post_by_id'),

    #search posts
     path('api/search/', SearchView.as_view(), name='search'),
]
