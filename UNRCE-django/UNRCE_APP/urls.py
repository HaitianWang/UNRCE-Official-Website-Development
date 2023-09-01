from django.urls import path, reverse_lazy
# Import the built-in views from Django with alias
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from .views import ForgetPasswordView, ResetPasswordView, IndexView, SignUpView, UploadImageView

app_name = "UNRCE_APP"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    
    path("login/", AuthLoginView.as_view(
            template_name="UNRCE_APP/login.html",
            success_url=reverse_lazy("UNRCE_APP:index"),
            redirect_authenticated_user=True,
        ), name="login"),
    
    path("logout/", AuthLogoutView.as_view(
            next_page=reverse_lazy("UNRCE_APP:index")
        ), name="logout"),
    
    path("signup/", SignUpView.as_view(), name="signup"),
    
    path("upload/", UploadImageView.as_view(), name="upload"),
    
    path('forget_password/', ForgetPasswordView.as_view(), name='forget_password'),
    path('reset_password/<uidb64>/<token>/', ResetPasswordView.as_view(), name='reset_password'),
]
