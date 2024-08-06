from django.urls import path
from .views import HomeView, ArticleDetailView,AddPostView, UpdatePostView, DeletePostView, AddCategoryView, CategoryView, CategoryListView, LikeView, CommentView, DeleteCommentView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('article/<int:pk>', ArticleDetailView.as_view(), name='article_detail'),
    path('add_post/', AddPostView.as_view(), name='add_post'),
    path('add_category/', AddCategoryView.as_view(), name='add_category'),
    path('article/update/<int:pk>', UpdatePostView.as_view(), name='update_post'),
    path('article/<int:pk>/delete', DeletePostView.as_view(), name='delete_post'),
    path('category/<str:cats>/', CategoryView, name='category'),
    path('category/', CategoryListView, name='category_list'),
    path('like/<int:pk>', LikeView, name='like_post'),
    path('post/<int:pk>/comment/', CommentView, name='add_comment'),
    path('comment/<int:pk>/remove/', DeleteCommentView, name='delete_comment'),
    
]