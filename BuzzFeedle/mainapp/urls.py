from django.urls import path
from . import views
from .views import HomeView, BlogEntries, ArticleDetailView, AddCommentView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', views.about_page, name='about_page'),
    path('contact/', views.contact_page, name='contact_page'),
    path('blog/', BlogEntries.as_view(), name='blog_page'),
    path('blog/<int:pk>/', ArticleDetailView.as_view(), name='post_detail'),
    path('blog/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('blog/<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('add_post/', views.post_blog, name='add_post'),
    path("category/<str:cats>/", views.cateogry_views, name='category'),
    path('category-list/', views.category_list_view, name='category-list' ),
    path('like/<int:pk>', views.LikeView, name='like_post'),    
    path('search/', views.search_bar, name="search_bar"),
    path('blog/<int:pk>/comment/',AddCommentView.as_view(), name='add_comment')

]