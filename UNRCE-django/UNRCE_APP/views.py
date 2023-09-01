from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from UNRCE_APP.models import Project 


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


def forgot_password(request):
    return render(request, 'UNRCE_APP/forgot-password.html')

def reset_password(request):
    return render(request, 'UNRCE_APP/reset-password.html')



class AddProjectView(View):
    def get(self, request):
        # You can render a form here to collect project data from the user
        # and then handle it in the post method
        return render(
            request,

            "UNRCE_APP/add_proj.html",  # Create a template for the form
        )

    def post(self, request):
        # Retrieve data from the form
        title = request.POST.get("title")
        description = request.POST.get("description")
        audience = request.POST.get("audience")
        # ... retrieve other fields ...

        # Create a new project instance
        new_project = Project(
    title=title,
    description=description,
    audience=audience,
    delivery_frequency=request.POST.get("delivery_frequency"),
    start_date=request.POST.get("start_date"),
    end_date=request.POST.get("end_date"),
    manager=request.user,  # Assuming you want to set the currently logged-in user as the manager
    # Other fields
    project_cover_image=request.FILES.get("project_cover_image"),
    language=request.POST.get("language"),
    format=request.POST.get("format"),
    web_link=request.POST.get("web_link"),
    policy_link=request.POST.get("policy_link"),
    results=request.POST.get("results"),
    lessons_learned=request.POST.get("lessons_learned"),
    key_messages=request.POST.get("key_messages"),
    relationship_to_rce_activities=request.POST.get("relationship_to_rce_activities"),
    funding=request.POST.get("funding"),
    priority_area_1=request.POST.get("priority_area_1"),
    priority_area_2=request.POST.get("priority_area_2"),
    priority_area_3=request.POST.get("priority_area_3"),
    priority_area_4=request.POST.get("priority_area_4"),
    priority_area_5=request.POST.get("priority_area_5"),
    disaster_risk_reduction=request.POST.get("disaster_risk_reduction"),
    traditional_knowledge=request.POST.get("traditional_knowledge"),
    agriculture=request.POST.get("agriculture"),
    arts=request.POST.get("arts"),
    curriculum_development=request.POST.get("curriculum_development"),
    ecotourism=request.POST.get("ecotourism"),
    forests_trees=request.POST.get("forests_trees"),
    plants_animals=request.POST.get("plants_animals"),
    waste=request.POST.get("waste"),
)



        # Save the new project instance to the database
        new_project.save()

        # Redirect to a success page or to the project list page
        return redirect("/projects/")  # Update the URL according to your project
