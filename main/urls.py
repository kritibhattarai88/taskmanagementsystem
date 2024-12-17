from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
urlpatterns = [
    path("", index, name='index'),
    path("login/", log_in, name='log_in'),
    path("register/", register, name='register'),
    path("create/", create_task, name="create_task"),
    path("assign/", assign_task, name="assign_task"),
    path("assigned/", assigned_task, name="assigned_task"),
    path("view/", view_task,name="view_task"),
    path("edit/<int:id>", edit, name="edit"),
    path("delete/<int:id>", delete_data, name="delete_data"),
    path("recycle/", recycle, name="recycle"),
    path("completed/<int:id>", completed, name="completed"),#mark as completed path
    path("completed_tasks/", completed_tasks, name="completed_tasks"),
    path("current_completed/<int:id>", current_completed, name="current_completed"),

    path("delete_current/<int:id>", delete_current, name="delete_current"),
    path("delete_assign/<int:id>", delete_assign, name="delete_assign"),
    path("restore/<int:id>", restore, name="restore"),
    path("logout/", log_out, name="log_out"),
    
    path("change_password/", change_password, name="change_password"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'), name='password_reset_complete'),

    
]
