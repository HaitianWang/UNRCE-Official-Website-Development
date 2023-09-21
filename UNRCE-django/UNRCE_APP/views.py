from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, views as auth_views
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from UNRCE_APP.models import Project 
from django.urls import reverse_lazy
from django.views.generic import CreateView

from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, HttpResponse
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.contrib.auth import get_user_model
from django.contrib import messages

# LoginRequiredMixin will check that user 
# is authenticated before rendering the template.
from django.contrib.auth.mixins import LoginRequiredMixin

from datetime import datetime
from .models import Image, CustomUser
from .forms import UploadImageForm, CustomUserCreationForm

from django.contrib.auth.views import LoginView
from django.contrib import messages
from .models import Project

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

def forgot_password(request):
  User = get_user_model()
  if request.method == "POST":
      email = request.POST['email']
      user = User.objects.filter(email=email).first()
      if not user:
          print('no user found')
          messages.error(request, 'No account with this email address exists.')
          return render(request, 'UNRCE_APP/forgot_password.html')
      elif user:
          print('found user')
          current_site = get_current_site(request)
          mail_subject = 'Reset your password.'
          message = render_to_string('UNRCE_APP/reset_password_email.html', {
              'user': user,
              'domain': current_site.domain,
              'uid': urlsafe_base64_encode(force_bytes(user.pk)),
              'token': account_activation_token.make_token(user),
          })
          
          # Send the email using SendGrid
          sg = SendGridAPIClient('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')  # Make sure to replace with your SendGrid API key
          email_msg = Mail(
              from_email='simonqiu4@gmail.com',
              to_emails=email,
              subject=mail_subject,
              html_content=message)
          response = sg.send(email_msg)
          print('sent message successfully')
          messages.success(request, 'A reset password link has been sent to your email.')
          return render(request, 'UNRCE_APP/email_sent_confirmation.html')

  return render(request, 'UNRCE_APP/forgot_password.html')

#display reset password page
def reset_password(request, uidb64, token):
  print("UID:", uidb64)
  print("TOKEN:", token)
  User = get_user_model()
  try:
      uid = force_str(urlsafe_base64_decode(uidb64))
      user = User.objects.get(pk=uid)
  except(TypeError, ValueError, OverflowError, User.DoesNotExist):
      user = None
  if user is not None and account_activation_token.check_token(user, token):
      if request.method == 'POST':
          password = request.POST['new_password']
          password2 = request.POST['retype_password']
          if password == password2:
              user.set_password(password)
              user.save()
              messages.success(request, 'Password reset successfully.')
              return redirect('login')
          else:
              messages.error(request, 'Passwords do not match.')
      return render(request, 'UNRCE_APP/reset_password.html')
  else:
      return HttpResponse('Reset password link is invalid!')



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
    {"name": "Disaster Risk Reduction", "id": "disaster_risk_reduction"},
    {"name": "Traditional Knowledge", "id": "traditional_knowledge"},
    {"name": "Agriculture", "id": "agriculture"},
    {"name": "Arts", "id": "arts"},
    {"name": "Curriculum Development", "id": "curriculum_development"},
    {"name": "Ecotourism", "id": "ecotourism"},
    {"name": "Forests Trees", "id": "forests_trees"},
    {"name": "Plants Animals", "id": "plants_animals"},
    {"name": "Waste", "id": "waste"}
]


        esd_options = [
            {"name": "Priority Action Area 1", "id": "priority_area_1"},
            {"name": "Priority Action Area 2", "id": "priority_area_2"},
            {"name": "Priority Action Area 3", "id": "priority_area_3"},
            {"name": "Priority Action Area 4", "id": "priority_area_4"},
            {"name": "Priority Action Area 5", "id": "priority_area_5"},
        ]
        context = {'sdgs': sdgs_options, 'audience_options': audience_options, 'delivery_frequency_options': delivery_frequency_options, 'esd_options': esd_options, 'esd_themes':esd_themes}

        return render(request, 'UNRCE_APP/create_project.html', context)
    
    def post(self, request):
          print(request.POST)        
          user = request.user

          new_project = Project(
            title = request.POST.get("title"),
            description = request.POST.get("description"),
            audience = request.POST.getlist("audience-options"),
    delivery_frequency=request.POST.get("delivery_frequency"),
    created_at=request.POST.get("start_date"),
    concluded_on =request.POST.get("end_date"),
   # manager=user,  # to set the currently logged-in user as the manager
    project_cover_image=request.FILES.get("project_cover_image"),
    language=request.POST.get("language"),
    format=request.POST.get("format"),
    web_link=request.POST.get("web_link"),
    policy_link=request.POST.get("policy_link"),
    results=request.POST.get("results"),
    lessons_learned=request.POST.get("lessons_learned"),
    key_messages=request.POST.get("key_messages"),
    relationship_to_rce_activities=request.POST.get("relationship_to_rce_activities"),
          funding=request.POST.get("funding"),)
        
    


        # Save the new project instance to the database
          new_project.save()
          return redirect("/upload/")  # Update the URL according to your project
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


