from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import (PostListView, 
	PostCreateView,
	PostUpdateView,
	PostDeleteView,
    CommentDeleteView,
    AllPostListView
)

urlpatterns = [
    path('', PostListView.as_view(), name ='blog-home'),

    path('post/<int:pk>/',views.DetailView,name='post-detail'),
    path('post/<int:pk>/upvote',views.UpVote,name='Up-Vote'),
    path('post/<int:pk>/downvote',views.DownVote,name='Down-Vote'),
    path('post/<int:pk>/novote',views.NoVote,name='No-Vote'),
    
    path('post/new/',PostCreateView.as_view(),name='post-create'),
    path('post/<int:pk>/update',PostUpdateView.as_view(),name='post-update'),
    path('post/<int:pk>/delete',PostDeleteView.as_view(),name='post-delete'),

    path('post/comment/<int:pk>/delete',CommentDeleteView.as_view(),name='comment-delete'),

    path('resource/', views.resource, name ='blog-resource'),
    path('contact/', views.contact, name ='blog-contact'),
    path('all_posts/',AllPostListView.as_view(), name ='all-posts')
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)