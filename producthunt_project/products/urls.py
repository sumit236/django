from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create, name='create'),
    path('<int:product_id>', views.details, name='details'),
    path('<int:product_id>/upvote', views.upvote, name='upvote'),
    path('<int:product_id>/user_specific_posts', views.user_specific_posts, name='user_specific_posts'),
    path('filterby_pubdate', views.filterby_pub_date, name='filterby_pubdate'),
    path('filterby_upvote', views.filterby_upvote, name='filterby_upvote'),
]
