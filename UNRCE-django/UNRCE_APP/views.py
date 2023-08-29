from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm

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
  
def ContactUs(response):
    return render(response, "UNRCE_APP/contactus.html", {})