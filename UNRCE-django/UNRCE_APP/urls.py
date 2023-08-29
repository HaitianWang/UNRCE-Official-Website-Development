from django.urls import path, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from .views import IndexView, SignUpView, UploadImageView
from . import views

app_name = "UNRCE_APP"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path(
        "login/",
        LoginView.as_view(
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
  # import UploadImageView from .views
  path("upload/", UploadImageView.as_view(), name="upload"),
  path('forgot-password/', views.forgot_password, name='forgot-password'),
  path('reset-password/', views.reset_password, name='reset-password'),
  path('contact-us/', views.contact_us, name='contact-us'),
  path('projects/', views.projects, name='projects'),

]
