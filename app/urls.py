from django.urls import path

from . import view


urlpatterns = [
	path('categories/',view.CategoryListCreateView.as_view(),name='category-list'),
	path('categories/<slug:slug>/',view.CategoryDetailView.as_view(),name='category-detail'),
	
	path('posts/',view.PostListCreateView.as_view(),name='post-list-create'),
	path('posts/me/',view.MyPostsView.as_view(),name='my-posts'),
	path('posts/<slug:slug>/',view.PostDetailView.as_view(),name='post-detail'),
	
	path('posts/<slug:slug>/comments/', view.CommentListCreateView.as_view(), name='comment-list'),
	path('comments/<int:id>/', view.CommentDeleteView.as_view(), name='comment-delete'),


]