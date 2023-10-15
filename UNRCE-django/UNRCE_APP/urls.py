from django.urls import path, reverse_lazy
from .views import CustomLoginView
from django.contrib.auth.views import LogoutView
from .views import IndexView, SignUpView, UploadImageView, CreateProject
from .views import CustomLoginView
from django.contrib.auth.views import LogoutView
from .views import IndexView, SignUpView, UploadImageView, edit_project, users_info
from . import views
from .forms import CustomAuthenticationForm
from django.urls import path, re_path

app_name = "UNRCE_APP"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path(
        "login/",
        CustomLoginView.as_view(
            authentication_form=CustomAuthenticationForm,
            template_name="UNRCE_APP/login.html",
            success_url=reverse_lazy("UNRCE_APP:index"),
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(next_page=reverse_lazy("UNRCE_APP:index")),
        name="logout",
    ),
    
    # Added signup view here
    path("signup/", SignUpView.as_view(), name="signup"),
      # Added upload view here, don't forget to
  # import UploadImageView from .views - hello
  path("upload/", UploadImageView.as_view(), name="upload"),
  path('forgot_password/', views.forgot_password, name='forgot_password'),
  re_path(r'^reset_password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', views.reset_password, name='reset_password_confirm'),
  path('contact-us/', views.contact_us, name='contact-us'),
  path('new_captcha/', views.new_captcha, name='new_captcha'),
  path('projects/', views.projects, name='projects'),
  path('specific_project/', views.specific_project, name='specific_project'),
  path("create_project/", CreateProject.as_view(), name="create_project"),
  path("myaccount/", views.myaccount, name="myaccount"),
  path("myaccount_edit/", views.myaccount_edit, name="myaccount_edit"),
  #path('approve_project/<int:project_id>/', views.approve_project, name='approve_project'),
  path('edit_project/<int:project_id>/', views.edit_project, name='edit_project'),
  path('users/', views.users_info, name='users'),
  path('admin/fetch_projects/', views.fetch_projects, name='fetch_projects'),
  path('user-search/', views.search_users, name='search_users'),
  path('delete-users/', views.delete_users, name='delete_users'),
  path('download-users/', views.download_users, name='download-users'),



]
