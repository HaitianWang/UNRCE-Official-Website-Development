from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.signing import TimestampSigner
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.urls import reverse
from django.conf import settings

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.forms import SetPasswordForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str






# LoginRequiredMixin will check that user 
# is authenticated before rendering the template.
from django.contrib.auth.mixins import LoginRequiredMixin

from datetime import datetime
from .models import Image
from .forms import UploadImageForm


class IndexView(View):
  def get(self, request):
    images = Image.objects.order_by("uploaded_date")
    return render(
      request,
      "UNRCE_APP/index.html",
      {
        "images": images,
      },
    )


class SignUpView(View):
  def get(self, request):
    return render(
      request,
      "UNRCE_APP/signup.html",
      {
        "form": UserCreationForm(),
      },
    )

  def post(self, request):
    form = UserCreationForm(request.POST)

    if form.is_valid():
      form.save()
      username = form.data["username"]
      password = form.data["password1"]
      user = authenticate(
        request,
        username=username,
        password=password,
      )
      if user:
        login(request, user)
      return redirect("/")

    return render(
      request,
      "UNRCE_APP/signup.html",
      {
        "form": form,
      },
    )


class UploadImageView(LoginRequiredMixin, View):
  # Not authenticated users will be redirected
  # to /login page if they try to access this view
  login_url = "/login/"

  def get(self, request):
    return render(
      request,
      "UNRCE_APP/upload.html",
      {
        "form": UploadImageForm(),
      },
    )

  def post(self, request):
    user = request.user
    if not user.is_authenticated:
      # Double check that user is authenticated
      raise Exception("User is not authenticated")

    # File, uploaded by user, will be available at request.FILES
    form = UploadImageForm(request.POST, request.FILES)

    if form.is_valid():
      # Creating a new image model instance
      img = Image(
        # get title from form.data
        title=form.data["title"],
        # get image from form.files
        image=form.files["image"],
        uploaded_date=datetime.now(),
        uploaded_by=user,
      )

      # save image to database
      img.save()

      # redirect to index page upon successful upload
      return redirect("/")

    # re-render form, show validation errors 
    return render(
      request,
      "UNRCE_APP/upload.html",
      {
        "form": form,
      },
    )
  







class ForgetPasswordView(View):
    # ...
    def post(self, request):
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(reverse('UNRCE_APP:reset_password', args=[uid, token]))
            # ... (rest of the logic remains same)

class ResetPasswordView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            token_generator = PasswordResetTokenGenerator()
            
            if token_generator.check_token(user, token):
                return render(request, 'UNRCE_APP/reset_password.html', {'user': user})
            else:
                return HttpResponse('Token is invalid or expired')
        except User.DoesNotExist:
            return HttpResponse('Token is invalid')

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('UNRCE_APP:login')
            return render(request, 'UNRCE_APP/reset_password.html', {'form': form, 'user': user})
        except User.DoesNotExist:
            return HttpResponse('Error resetting password')

















