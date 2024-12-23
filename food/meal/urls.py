from django.urls import path

from .views import *

urlpatterns = [
    path('', FoodHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', FoodCategory.as_view(), name='category'),
    path('edit/<slug:post_slug>/', EditPostView.as_view(), name='edit_post'),
    path('unpublished/', UnpublishedPostsView.as_view(), name='unpublished_posts'),
]
