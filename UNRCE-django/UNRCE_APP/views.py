from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, views as auth_views
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from UNRCE_APP.models import Project, ProjectImage
# ProjectImage

from django.urls import reverse_lazy
from django.views.generic import CreateView

# LoginRequiredMixin will check that user 
# is authenticated before rendering the template.
from django.contrib.auth.mixins import LoginRequiredMixin

from datetime import datetime
from .models import Image, CustomUser
from .forms import UploadImageForm, CustomUserCreationForm

from django.contrib.auth.views import LoginView
from django.contrib import messages
from .models import Project, SDG, ProjectSDG, ESD, ProjectESD, ProjectPriorityArea, PriorityArea

class CustomLoginView(LoginView):
    
    def form_valid(self, form):
        # Add any custom logic here. 
        # For instance, log when a user successfully logs in.
        messages.success(self.request, "Logged in successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Add any custom logic for when the form is invalid.
        # For instance, log when a login attempt fails.
        messages.error(self.request, "Failed to log in. Please check your credentials.")
        return super().form_invalid(form)
 
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
                "form": CustomUserCreationForm(),
            },
        )
    def get(self, request):
        return render(
            request,
            "UNRCE_APP/signup.html",
            {
                "form": CustomUserCreationForm(),
            },
        )

    def post(self, request):
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')  # Get the email from cleaned_data
            password = form.cleaned_data.get('password1') 
            user = authenticate(
                request,
                email=email,   # Use email to authenticate
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

#display forgot password page
def forgot_password(request):
    return render(request, 'UNRCE_APP/forgot-password.html')
#display reset password page
def reset_password(request):
    return render(request, 'UNRCE_APP/reset-password.html')
def contact_us(request):
    return render(request, 'UNRCE_APP/contact-us.html')
#display projects page
def projects(request):
    project_query = Project.objects.all()   # Store the rows from the "Project" table, and store them in project_query
    return render(request, 'UNRCE_APP/projects.html', {'project_query': project_query})   # Dictionary Containing data to send. Includes the project_query variable passed with name "project_query"
# My Account Page
def myaccount(request):
    return render(request, 'UNRCE_APP/myaccount.html')
# My Account Page
def myaccount_edit(request):
    return render(request, 'UNRCE_APP/myaccount_edit.html')

# This is a function to return a list of featured projects by recently added
# def index(request):
#     # Just an example: getting the last 5 projects.
#     # Adjust the query to fetch projects as per your criteria.
#     featured_projects = Project.objects.all().order_by('-created_date')[:5]
    
#     return render(request, 'UNRCE_APP/index.html', {
#         'featured_projects': featured_projects
#     })

#return index page
def index(request):
    return render(request, 'UNRCE_APP/index.html')
#display information from the chosen project page
# hello 
def specific_project(request):
    img_src = request.GET.get('img', '') 
    title_text = request.GET.get('title', '')
    return render(request, 'UNRCE_APP/specific_project.html', {'img_src': img_src, 'title_text': title_text})


class CreateProject(View):

    
    
    def get(self, request):
        sdgs_options = ['SDG1', 'SDG2', 'SDG3', 'SDG4', 'SDG5', 'SDG6', 'SDG7', 'SDG8', 'SDG9', 'SDG10','SDG11', 'SDG12', 'SDG13', 'SDG14', 'SDG15', 'SDG16', 'SDG17']  # List of SDGs
        

        delivery_frequency_options = [
        {"name": "Monthly", "id": "monthly"},
        {"name": "Quarterly", "id": "quarterly"},
        {"name": "Biannually", "id": "biannually"},
        {"name": "Annually", "id": "annually"},
        {"name": "Ongoing", "id": "ongoing"},
        {"name": "Once", "id": "once"},
        {"name": "Opportunistic/Irregularly", "id": "irregular"},
        {"name": "Permanent/On demand", "id": "on_demand"}]


        audience_options = [
    {"name": "General", "id": "general"},
    {"name": "Particular target Audience (Please specify)", "id": "target"},
    {"name": "Adults", "id": "adults"},
    {"name": "Tertiary students", "id": "tertiary"},
    {"name": "High school age", "id": "high_school"},
    {"name": "Primary School age", "id": "primary_school"},
    {"name": "Early years", "id": "early_years"},
    {"name": "Adults >60 please", "id": "adults_60"}
]

        esd_themes = [
    {"description": "Disaster Risk Reduction", "name": "disaster_risk_reduction"},
    {"description": "Traditional Knowledge", "name": "traditional_knowledge"},
    {"description": "Agriculture", "name": "agriculture"},
    {"description": "Arts", "name": "arts"},
    {"description": "Curriculum Development", "name": "curriculum_development"},
    {"description": "Ecotourism", "name": "ecotourism"},
    {"description": "Forests Trees", "name": "forests_trees"},
    {"description": "Plants Animals", "name": "plants_animals"},
    {"description": "Waste", "name": "waste"}
]


        pa_options = [
            {"description": "Priority Action Area 1", "name": "priority_area_1"},
            {"description": "Priority Action Area 2", "name": "priority_area_2"},
            {"description": "Priority Action Area 3", "name": "priority_area_3"},
            {"description": "Priority Action Area 4", "name": "priority_area_4"},
            {"description": "Priority Action Area 5", "name": "priority_area_5"},
        ]
        context = {'sdgs': sdgs_options, 'audience_options': audience_options, 'delivery_frequency_options': delivery_frequency_options, 'pa_options': pa_options, 'esd_themes':esd_themes}

        return render(request, 'UNRCE_APP/create_project.html', context)
    
    def post(self, request):
                
        sdgs_options = ['goal_1','goal_2','goal_3','goal_4','goal_5','goal_6','goal_7','goal_8','goal_9','goal_10','goal_11','goal_12','goal_13','goal_14','goal_15','goal_16','goal_17']  

        pa_options = [
            {"description": "Priority Action Area 1", "name": "priority_area_1"},
            {"description": "Priority Action Area 2", "name": "priority_area_2"},
            {"description": "Priority Action Area 3", "name": "priority_area_3"},
            {"description": "Priority Action Area 4", "name": "priority_area_4"},
            {"description": "Priority Action Area 5", "name": "priority_area_5"},
        ]

        esd_themes = [
    {"description": "Disaster Risk Reduction", "name": "disaster_risk_reduction"},
    {"description": "Traditional Knowledge", "name": "traditional_knowledge"},
    {"description": "Agriculture", "name": "agriculture"},
    {"description": "Arts", "name": "arts"},
    {"description": "Curriculum Development", "name": "curriculum_development"},
    {"description": "Ecotourism", "name": "ecotourism"},
    {"description": "Forests Trees", "name": "forests_trees"},
    {"description": "Plants Animals", "name": "plants_animals"},
    {"description": "Waste", "name": "waste"}
]

        print(request.POST)        
        user = request.user

        new_project = Project(
        title=request.POST.get("title"),
        description=request.POST.get("description"),
        audience=request.POST.getlist("audience-options"),
        delivery_frequency=request.POST.get("delivery_frequency"),
        created_at=request.POST.get("start_date"),
        concluded_on=request.POST.get("end_date"),
        #manager=user,  # to set the currently logged-in user as the manager
        #project_cover_image=request.FILES.get("project_cover_image"),
        language=request.POST.get("language"),
        format=request.POST.get("format"),
        web_link=request.POST.get("web_link"),
        policy_link=request.POST.get("policy_link"),
        results=request.POST.get("results"),
        lessons_learned=request.POST.get("lessons_learned"),
        key_messages=request.POST.get("key_messages"),
        relationship_to_rce_activities=request.POST.get("relationship_to_rce_activities"),
        funding=request.POST.get("funding")
    )

    # Save the new project instance to the database
        new_project.save()

        for sdg in sdgs_options:
            relationship_value = request.POST.get("sdg_relationship_" + "SDG" + sdg.split('_')[-1])
            print(f"Checking SDG: {sdg}, Relationship Value: {relationship_value}")

            if relationship_value:
                try:
                    sdg_instance = SDG.objects.get(sdg=sdg)
                except SDG.DoesNotExist:
                    print(f"SDG {sdg} does not exist in the database! and RV == {relationship_value}")
                    continue

                project_sdg = ProjectSDG(project=new_project, goal=sdg_instance, relationship_type=relationship_value)
                print(sdg + " heyyyyyyyyyyyyyyyyyy")
                project_sdg.save()


        for esd in esd_themes:
            relationship_value = request.POST.get(esd["name"])

            if relationship_value:
                try:
                    esd_instance = ESD.objects.get(name=esd["name"])
                    project_esd = ProjectESD(project=new_project, esd=esd_instance, relationship_type=relationship_value)
                    project_esd.save()
                except ESD.DoesNotExist:
                    print(f"ESD {esd} does not exist in the database! and RV == {relationship_value}")
                    continue

                


        for pa in pa_options:
            relationship_value = request.POST.get(pa["name"])

            if relationship_value:
                try:
            # Assuming you're fetching the ESD instance based on its name
                    pa_instance = PriorityArea.objects.get(name=pa["name"])
            
            # Move the code that uses esd_instance inside the try block
                    project_priorityarea = ProjectPriorityArea(project=new_project, priority_area=pa_instance, relationship_type=relationship_value)
                    print(pa['name'] + " processed!")
                    project_priorityarea.save()
            
                except PriorityArea.DoesNotExist:
                    print(f"PriorityArea {pa['name']} does not exist in the database! and RV == {relationship_value}")
                    continue




        return render(request, 'UNRCE_APP/contact-us.html')

    # Now that the project has been saved, you can save its image
        #if 'imageUpload' in request.FILES:  # Making sure an image was uploaded
        #    project_image = ProjectImage(project=new_project, image=request.FILES.get('imageUpload'))
        #project_image.save()

        #return redirect("/upload/")  # Update the URL according to your project

"""
          sdgs = ['SDG1', 'SDG2', 'SDG3', 'SDG4', 'SDG5']  # List of SDGs
          for sdg in sdgs:
            sdg_id = sdg.id
            relationship_type = request.POST.get(f'sdg_relationship_{sdg_id}', '')

            if relationship_type:
              sdg = SDG.objects.get(id=sdg_id)

            # Create a ProjectSDG instance to associate SDG with Project
            project_sdg = ProjectSDG.objects.create(project=new_project, sdg=sdg, relationship_type=relationship_type)

        # Redirect to a success page or to the project list page

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
    waste=request.POST.get("waste"),"""


