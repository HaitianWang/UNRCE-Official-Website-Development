from django.db.models import Q
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.views import View

from .forms import ProjectForm, UploadImageForm, CustomUserCreationForm, UpdateAccountForm
from .models import Project, CustomUser, Project, SDG, ProjectSDG, ESD, ProjectESD, ProjectPriorityArea, PriorityArea, Image
from .tokens import account_activation_token

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from captcha.models import CaptchaStore

from datetime import datetime

import csv



User = get_user_model()

def search_users(request):
    if request.method != 'GET':
        # Return an empty queryset by default
        return render(
            request, {
                'users': CustomUser.objects.none(),
                "search_query": request.GET.get('search_query', ''),
            }
        )
    
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

    return render(
        request, 
        'UNRCE_APP/user_search.html', 
        { 'users': users, 'search_query': search_query }
    )


def new_captcha(request):
    """Return new captcha image and key."""
    captcha_key = CaptchaStore.generate_key()
    captcha_image_url = reverse('captcha-image', kwargs={'key': captcha_key})
    return JsonResponse({'captcha_image_url': captcha_image_url, 'captcha_key': captcha_key})

class CustomLoginView(LoginView):
    
    def form_valid(self, form):
        captcha_value = self.request.POST.get('captcha_0')
        captcha_key = self.request.POST.get('captcha_1')

        # Check the captcha
        captcha_check = CaptchaStore.objects.filter(response__iexact=captcha_value, hashkey=captcha_key)
        if not captcha_check.exists():
            messages.error(self.request, "Captcha is incorrect.")
            return self.form_invalid(form)  # Changed from super().form_invalid(form)
        
        messages.success(self.request, "Logged in successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        captcha_key = CaptchaStore.generate_key()  # Always regenerate the captcha_key
        messages.error(self.request, "Failed to log in. Please check your credentials.")
        return render(
            self.request,
            "UNRCE_APP/login.html",{
                "form": form,
                "captcha_key": captcha_key
            }
        )

    def get(self, request, *args, **kwargs):
        captcha_key = CaptchaStore.generate_key()
        return render(
            request, 
            "UNRCE_APP/login.html", {
                "captcha_key": captcha_key, 
                "form": self.get_form()
            },
        ) 

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        
        if form.is_valid():
            return self.form_valid(form)
        
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
            "UNRCE_APP/signup.html",{
                "form": CustomUserCreationForm(),
                "captcha_key": captcha_key,
            },
        )

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        captcha_value = request.POST.get('captcha_0')
        captcha_key = request.POST.get('captcha_1')
        captcha_check = CaptchaStore.objects.filter(response__iexact=captcha_value, hashkey=captcha_key)

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

        if not form.is_valid():
            messages.error(request, "Form invalid!")
            captcha_key = CaptchaStore.generate_key()  # Regenerate the captcha_key
            return render(
                request,
                "UNRCE_APP/signup.html",
                {
                    "form": form,  # Use the same form instance to retain the user's input
                    "captcha_key": captcha_key,
                },
            )

        email = form.cleaned_data.get('email')  # Get email address
        
        # No need to query the database anymore
        user = form.save(commit=False)  # Create but do not save user object
        user.is_active = False  # Make user inactive until they confirm email
        user.save()

        # Generate token and send email
        current_site = get_current_site(request)
        mail_subject = 'Activate your account.'
        message = render_to_string(
            'UNRCE_APP/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }
        )

        # Send the email using SendGrid
        sg = SendGridAPIClient('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')  # Make sure to replace with your SendGrid API key
        email_msg = Mail(
            from_email='Rce.uwa@gmail.com',
            to_emails=email,
            subject=mail_subject,
            html_content=message)
        response = sg.send(email_msg)
        messages.success(request, 'A reset password link has been sent to your email.')

        return render(request, 'UNRCE_APP/account_activation_sent.html')


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        return HttpResponse('Activation link is invalid!')
    
    if not account_activation_token.check_token(user, token):
        return HttpResponse('Activation link is invalid!')
    
    user.is_active = True
    user.email_confirmed = True
    user.save()
    messages.success(request, 'Account activated successfully.')
    login(request, user)
    return redirect('UNRCE_APP:myaccount')
        

        
def forgot_password(request):
    User = get_user_model()
    if request.method != "POST":
        return render(request, 'UNRCE_APP/forgot_password.html')
    
    email = request.POST['email']
    user = User.objects.filter(email=email).first()

    if not user:
        messages.error(request, 'No account with this email address exists.')
        return render(request, 'UNRCE_APP/forgot_password.html')
    
    current_site = get_current_site(request)
    mail_subject = 'Reset your password.'
    message = render_to_string(
        'UNRCE_APP/reset_password_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        }
    )
    
    # Send the email using SendGrid, TODO: Include the API Key in the settings file
    sg = SendGridAPIClient('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') 
    email_msg = Mail(
        from_email='Rce.uwa@gmail.com',
        to_emails=email,
        subject=mail_subject,
        html_content=message,
    )
    response = sg.send(email_msg)
    messages.success(request, 'A reset password link has been sent to your email.')
    return render(request, 'UNRCE_APP/email_sent_confirmation.html')

#display reset password page
def reset_password(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is None or not account_activation_token.check_token(user, token):
        return HttpResponse('Reset password link is invalid!')
    
    if request.method != 'POST':
        return render(request, 'UNRCE_APP/reset_password.html')    
    
    password = request.POST['new_password']
    password2 = request.POST['retype_password']
    
    if password != password2:
        messages.error(request, 'Passwords do not match.')
        return render(request, 'UNRCE_APP/reset_password.html')
    
    user.set_password(password)
    user.save()
    messages.success(request, 'Password reset successfully.')
    return redirect('UNRCE_APP:login')
     

class IndexView(View):
    def get(self, request):
        images = Image.objects.order_by("uploaded_date")
        return render(
            request,
            "UNRCE_APP/index.html",
            {"images": images},
        )


class UploadImageView(LoginRequiredMixin, View):
    # Not authenticated users will be redirected
    # to /login page if they try to access this view
    login_url = "/login/"

    def get(self, request):
        return render(
            request,
            "UNRCE_APP/upload.html",
            {"form": UploadImageForm()},
        )

    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            raise Exception("User is not authenticated")

        # File, uploaded by user, will be available at request.FILES
        form = UploadImageForm(request.POST, request.FILES)

        if not form.is_valid():
            # re-render form, show validation errors 
            return render(
                request,
                "UNRCE_APP/upload.html",
                {"form": form},
            )
        
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

def contact_us(request):
    return render(request, 'UNRCE_APP/contact-us.html')

@staff_member_required(login_url="UNRCE_APP:login")
def users_info(request):
    return render(request, 'UNRCE_APP/users_info.html')

def projects(request):
    # Dictionary Containing data to send. Includes rows from the "Project" table sent as "project_query"
    return render(request, 'UNRCE_APP/projects.html', {'project_query': Project.objects.all()})   

@login_required
def myaccount(request):
    return render(request, 'UNRCE_APP/myaccount.html', {'user': request.user})

# Edit my Account Page
@login_required
def myaccount_edit(request):
    if request.method == 'POST':
        form = UpdateAccountForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            return redirect('/myaccount')
    else:
        form = UpdateAccountForm(instance=request.user)
    return render(request, 'UNRCE_APP/myaccount_edit.html', {'form': form})

# This is a function to return a list of featured projects by recently added
# def index(request):
#     # Just an example: getting the last 5 projects.
#     # Adjust the query to fetch projects as per your criteria.
#     featured_projects = Project.objects.all().order_by('-created_date')[:5]
    
#     return render(request, 'UNRCE_APP/index.html', {
#         'featured_projects': featured_projects
#     })


def index(request):
    return render(request, 'UNRCE_APP/index.html')

def specific_project(request):
    img_src = request.GET.get('img', '') 
    title_text = request.GET.get('title', '')
    return render(request, 'UNRCE_APP/specific_project.html', {'img_src': img_src, 'title_text': title_text})


class CreateProject(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request):
        sdgs_options = [
            'SDG1 - No Poverty', 'SDG2 - Zero Hunger', 'SDG3 - Good Health and Well-being', 
            'SDG4 - Quality Education', 'SDG5 - Gender Equality', 'SDG6 - Clean Water and Sanitation', 
            'SDG7 - Affordable and Clean Energy', 'SDG8 - Decent Work and Economic Growth', 
            'SDG9 - Industry, Innovation and Infrastructure', 'SDG10 - Reduced Inequalities',
            'SDG11 - Sustainable Cities and Communities', 'SDG12 - Responsible Consumption and Production', 
            'SDG13 - Climate Action', 'SDG14 - Life Below Water', 'SDG15 - Life on Land', 
            'SDG16 - Peace, Justice and Strong Institutions', 'SDG17 - Partnerships for the Goals'
        ]  

        delivery_frequency_options = [
            {"name": "Monthly", "id": "monthly"},
            {"name": "Quarterly", "id": "quarterly"},
            {"name": "Biannually", "id": "biannually"},
            {"name": "Annually", "id": "annually"},
            {"name": "Ongoing", "id": "ongoing"},
            {"name": "Once", "id": "once"},
            {"name": "Opportunistic/Irregularly", "id": "irregular"},
            {"name": "Permanent/On demand", "id": "on_demand"}
        ]

        audience_options = [
            {"name": "General", "id": "general"},
            {"name": "Adults", "id": "adults"},
            {"name": "Tertiary students", "id": "tertiary"},
            {"name": "High school age", "id": "high_school"},
            {"name": "Primary School age", "id": "primary_school"},
            {"name": "Early years", "id": "early_years"},
            {"name": "Adults >60", "id": "adults_60"}
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

        context = {
            'sdgs': sdgs_options, 
            'audience_options': audience_options, 
            'delivery_frequency_options': delivery_frequency_options, 
            'pa_options': pa_options, 
            'esd_themes':esd_themes
        }

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
     
        user = request.user
        action = request.POST.get("action", "save")  # Default to 'save' if 'action' isn't present
        status = "submitted" if action == "submit" else "draft"

        new_project = Project(
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            audience=request.POST.getlist("audience-options"),
            created_at=request.POST.get("start_date"),
            concluded_on=request.POST.get("end_date"),
            owner=user,  # to set the currently logged-in user as the manager
            #project_cover_image=request.FILES.get("imageUpload"),
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
        


        delivery_frequency=request.POST.get("delivery_frequency"),
        if delivery_frequency is not None:
            new_project.delivery_frequency = delivery_frequency

        # Save the new project instance to the database
        new_project.save()

        for sdg in sdgs_options:
            relationship_value = request.POST.get("sdg_relationship_" + "SDG" + sdg.split('_')[-1])

            if not relationship_value:
                continue

            try:
                sdg_instance = SDG.objects.get(sdg=sdg)
            except SDG.DoesNotExist:
                continue

            project_sdg = ProjectSDG(project=new_project, goal=sdg_instance, relationship_type=relationship_value)
            project_sdg.save()

        for esd in esd_themes:
            relationship_value = request.POST.get(esd["name"])

            if not relationship_value:
                continue

            try:
                esd_instance = ESD.objects.get(name=esd["name"])
            except ESD.DoesNotExist:
                continue

            project_esd = ProjectESD(project=new_project, esd=esd_instance, relationship_type=relationship_value)
            project_esd.save()

        for pa in pa_options:
            relationship_value = request.POST.get(pa["name"])

            if not relationship_value:
                continue
            
            try:
                # Assuming you're fetching the ESD instance based on its name
                pa_instance = PriorityArea.objects.get(name=pa["name"])
            except PriorityArea.DoesNotExist:
                continue
            
            project_priorityarea = ProjectPriorityArea(project=new_project, priority_area=pa_instance, relationship_type=relationship_value)
            project_priorityarea.save()

        return render(request, 'UNRCE_APP/contact-us.html')
    
@login_required
def edit_project(request, project_id):

    project = get_object_or_404(Project, pk=project_id)

    user = request.user
    if user != project.owner and not (user.is_staff() and user.is_active()):
        raise PermissionDenied

    if request.method != 'POST':
        return render(request, 'UNRCE_APP/edit_project.html', {'form': ProjectForm(instance=project)})
    
    form = ProjectForm(request.POST, instance=project)

    if not form.is_valid():
        return render(request, 'UNRCE_APP/edit_project.html', {'form': form})
    
    form.save()

    # Redirect to a success page or update the current page as needed
    return redirect('/myaccount/')  

    

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


@staff_member_required(login_url="UNRCE_APP:login")
def delete_users(request):
    if request.method == "POST":
        user_ids = request.POST.getlist("user_ids") # "user_ids" matches the checkbox name
        CustomUser.objects.filter(id__in=user_ids).delete()
        return HttpResponseRedirect('/user-search/') # Redirect back to the search page
    
@staff_member_required(login_url="UNRCE_APP:login")
def download_users(request):
    search_query = request.GET.get('search_query', '')
    
    if search_query:
        users = User.objects.filter(user_name__icontains=search_query)  # Assuming user_name is the field you're searching
    else:
        users = User.objects.all()

    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    writer = csv.writer(response)
    # Write header
    writer.writerow(['User Name', 'Email', 'Organisation', 'Role', 'Interested Projects', 'Interested SDGs', 'RCE Hub'])
    # Write user data
    for user in users:
        writer.writerow([
            user.user_name,
            user.email,
            user.organisation.org_name if user.organisation else 'None',
            user.role_organisation,
            ', '.join([proj.title for proj in user.interested_projects.all()]),
            ', '.join([sdg.sdg for sdg in user.interested_sdgs.all()]),
            user.rce_hub.hub_name if user.rce_hub else 'None'
        ])

    return response