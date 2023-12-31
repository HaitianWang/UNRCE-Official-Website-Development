from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser
from .models import Project #, Image
from .models import SDG

from django.core.exceptions import ValidationError

# We use Django's built-in ModelForm class
# class UploadImageForm(forms.ModelForm):
#   class Meta:
#     model = Image
#     # only image and title fields from the Image
#     # model will be available to user
#     fields = ["image", "title"]
#     # Let's play with it a little to
#     # get a taste of Django widgets
#     widgets = {
#       "title": forms.Textarea(
#         attrs={
#           "cols": 60,
#           "rows": 3,
#         }
#       ),
#     }

#Create a form that will use email for authentication 
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email",)
        labels = {
            "email": "Email",
        }

    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     if re.search(r'[0-9!@#$%^&*(),.?":{}|<>]', email):
    #         raise ValidationError("Name should not contain numbers or special characters.")
    #     return email


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'


class UserSearchForm(forms.Form):
    search_query = forms.CharField(label='Search Users', max_length=100, required=False)


# Update the user's details
class UpdateAccountForm(forms.ModelForm):
    emails_enabled = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(),
        initial=True
    )

    interested_sdgs = forms.ModelMultipleChoiceField(
        queryset=SDG.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Select your SDGs of interest",
    )

    class Meta:
        model = CustomUser
        fields = ['name', 'org', 'emails_enabled', 'rce_hub2', 'role_organisation', 'interested_sdgs']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if any(char.isdigit() for char in name) or not name.isalpha():
            raise ValidationError("Name should only contain letters and should not include any numbers or special characters.")
        return name
