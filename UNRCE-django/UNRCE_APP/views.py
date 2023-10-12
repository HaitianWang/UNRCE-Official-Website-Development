from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProjectForm
from django.contrib.auth import authenticate, login, views as auth_views
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from UNRCE_APP.models import Project, ProjectImage, CustomUser
from django.http import JsonResponse
# ProjectImage

from django.http import HttpResponseRedirect
from django.shortcuts import render


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

from captcha.models import CaptchaStore

# LoginRequiredMixin will check that user 
# is authenticated before rendering the template.
from django.contrib.auth.mixins import LoginRequiredMixin

from datetime import datetime
from .models import Image, CustomUser
from .forms import UploadImageForm, CustomUserCreationForm

from django.contrib.auth.views import LoginView
from django.contrib import messages
from .models import Project, SDG, ProjectSDG, ESD, ProjectESD, ProjectPriorityArea, PriorityArea

# views.py
from .models import CustomUser
from django.db.models import Q

def search_users(request):
    if request.method == 'GET':
        search_query = request.GET.get('search_query', '')

        # Perform the search query based on user input
        users = CustomUser.objects.filter(
            Q(email__icontains=search_query) |
            Q(user_name__icontains=search_query) |
            Q(interested_projects__title__icontains=search_query) |
            Q(organisation__org_name__icontains=search_query) |
            Q(role_organisation__icontains=search_query) |
            Q(interested_sdgs__sdg__icontains=search_query) |
            Q(rce_hub__hub_name__icontains=search_query)
        ).distinct()
    else:
        users = CustomUser.objects.none()  # Return an empty queryset by default

    return render(request, 'UNRCE_APP/user_search.html', {'users': users})


from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.contrib import messages 
#from .models import CaptchaStore  # Make sure to import CaptchaStore if not already done

class CustomLoginView(LoginView):
    
    def form_valid(self, form):
        captcha_value = self.request.POST.get('captcha_0')
        captcha_key = self.request.POST.get('captcha_1')

        # Check the captcha
        captcha_check = CaptchaStore.objects.filter(response=captcha_value, hashkey=captcha_key)
        if not captcha_check.exists():
            messages.error(self.request, "Captcha is incorrect.")
            return self.form_invalid(form)  # Changed from super().form_invalid(form)
        
        # Add any custom logic here. 
        # For instance, log when a user successfully logs in.
        messages.success(self.request, "Logged in successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Add any custom logic for when the form is invalid.
        # For instance, log when a login attempt fails.
        captcha_key = CaptchaStore.generate_key()  # Always regenerate the captcha_key
        messages.error(self.request, "Failed to log in. Please check your credentials.")
        return render(
            self.request,
            "UNRCE_APP/login.html",
            {
                "form": form,
                "captcha_key": captcha_key
            }
        )

    def get(self, request, *args, **kwargs):
        captcha_key = CaptchaStore.generate_key()
        return render(
            request, 
            "UNRCE_APP/login.html", 
            {
                "captcha_key": captcha_key, 
                "form": self.get_form()
            },
        ) 

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        
        if form.is_valid():
            return self.form_valid(form)
        else:
            captcha_key = CaptchaStore.generate_key()
            return render(
                request,
                "UNRCE_APP/login.html",
                {
                    "form": form,
                    "captcha_key": captcha_key
                }
            )


class SignUpView(View):

    def get(self, request):
        captcha_key = CaptchaStore.generate_key()
        return render(
            request,
            "UNRCE_APP/signup.html",
            {
                "form": CustomUserCreationForm(),
                "captcha_key": captcha_key,
            },
        )

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        captcha_value = request.POST.get('captcha_0')
        captcha_key = request.POST.get('captcha_1')
    
        captcha_check = CaptchaStore.objects.filter(response=captcha_value, hashkey=captcha_key)
        
        if not captcha_check.exists():
            messages.error(request, "Captcha is incorrect.")
            captcha_key = CaptchaStore.generate_key()  # Regenerate the captcha_key
            return render(
                request,
                "UNRCE_APP/signup.html",
                {
                    "form": form,  # Use the same form instance to retain the user's input
                    "captcha_key": captcha_key,
                },
            )

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

        # If form is not valid, also regenerate the captcha_key
        captcha_key = CaptchaStore.generate_key()
        return render(
            request,
            "UNRCE_APP/signup.html",
            {
                "form": form,
                "captcha_key": captcha_key,
            },
        )

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
              return redirect('UNRCE_APP:login')
          else:
              messages.error(request, 'Passwords do not match.')
      return render(request, 'UNRCE_APP/reset_password.html')
  else:
      return HttpResponse('Reset password link is invalid!')



def contact_us(request):
    return render(request, 'UNRCE_APP/contact-us.html')
def users_info(request):
    return render(request, 'UNRCE_APP/users_info.html')
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
        sdgs_options = ['SDG1 - No Poverty', 'SDG2 - Zero Hunger', 'SDG3 - Good Health and Well-being', 
                        'SDG4 - Quality Education', 'SDG5 - Gender Equality', 'SDG6 - Clean Water and Sanitation', 
                        'SDG7 - Affordable and Clean Energy', 'SDG8 - Decent Work and Economic Growth', 
                        'SDG9 - Industry, Innovation and Infrastructure', 'SDG10 - Reduced Inequalities',
                        'SDG11 - Sustainable Cities and Communities', 'SDG12 - Responsible Consumption and Production', 
                        'SDG13 - Climate Action', 'SDG14 - Life Below Water', 'SDG15 - Life on Land', 
                        'SDG16 - Peace, Justice and Strong Institutions', 'SDG17 - Partnerships for the Goals']  # List of SDGs
        

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
            {"description": "Advancing policy Direct", "name": "priority_area_1"},
            {"description": "Transforming learning and training environments Direct", "name": "priority_area_2"},
            {"description": "Developing capacities of educators and trainers Direct", "name": "priority_area_3"},
            {"description": "Mobilizing youth Direct", "name": "priority_area_4"},
            {"description": "Accelerating sustainable solutions at local level Direct", "name": "priority_area_5"},
        ]

        context = {'sdgs': sdgs_options, 'audience_options': audience_options, 'delivery_frequency_options': delivery_frequency_options, 'pa_options': pa_options, 'esd_themes':esd_themes}

        return render(request, 'UNRCE_APP/create_project.html', context)
    
    def post(self, request):
                
        sdgs_options = ['goal_1','goal_2','goal_3','goal_4','goal_5','goal_6','goal_7','goal_8','goal_9','goal_10','goal_11','goal_12','goal_13','goal_14','goal_15','goal_16','goal_17']  

        pa_options = [
            {"description": "Advancing policy Direct", "name": "priority_area_1"},
            {"description": "Transforming learning and training environments Direct", "name": "priority_area_2"},
            {"description": "Developing capacities of educators and trainers Direct", "name": "priority_area_3"},
            {"description": "Mobilizing youth Direct", "name": "priority_area_4"},
            {"description": "Accelerating sustainable solutions at local level Direct", "name": "priority_area_5"},
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

        action = request.POST.get("action", "save")  # Default to 'save' if 'action' isn't present
        status = "submitted" if action == "submit" else "draft"


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
        funding=request.POST.get("funding"),
        status=status
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
    
def edit_project(request, project_id):



    project = get_object_or_404(Project, pk=project_id)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            # Redirect to a success page or update the current page as needed
            return redirect('UNRCE_APP/contact-us.html')  # Change 'success_page' to your desired URL name

    else:
        form = ProjectForm(instance=project)

    return render(request, 'UNRCE_APP/edit_project.html', {'form': form})

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




def fetch_projects(request):
    query = request.GET.get('q', '')
    projects = Project.objects.filter(title__icontains=query)
    return JsonResponse([{'id': proj.id, 'text': proj.title} for proj in projects], safe=False)



def delete_users(request):
    if request.method == "POST":
        user_ids = request.POST.getlist("user_ids") # "user_ids" matches the checkbox name
        CustomUser.objects.filter(id__in=user_ids).delete()
        return HttpResponseRedirect('/user-search/') # Redirect back to the search page