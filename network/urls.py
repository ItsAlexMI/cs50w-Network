
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("new_post/", views.new_post, name="new_post"),
    path("edit_post/<int:post_id>/", views.edit_post, name="edit_post"),
    path('toggle-like/<int:post_id>/', views.toggle_like, name='toggle_like'),
    path('get-like-count/<int:post_id>/', views.get_like_count, name='get_like_count'),
    path("comment/<int:post_id>/", views.comment, name="comment"),
    path("delete_comment/<int:comment_id>/", views.delete_comment, name="delete_comment"),
     path('delete-post/<int:post_id>/', views.delete_post, name='delete_post'),
    path("seguir_perfil/<str:username>/", views.seguir_perfil, name="seguir_perfil"),
    path("dejar_seguir_perfil/<str:username>/", views.dejar_seguir_perfil, name="dejar_seguir_perfil"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("following/", views.following, name="following"),

]
