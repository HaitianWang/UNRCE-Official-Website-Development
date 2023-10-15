from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser
from .models import Image, Project


# We use Django's built-in ModelForm class
class UploadImageForm(forms.ModelForm):
  class Meta:
    model = Image
    # only image and title fields from the Image
    # model will be available to user
    fields = ["image", "title"]
    # Let's play with it a little to
    # get a taste of Django widgets
    widgets = {
      "title": forms.Textarea(
        attrs={
          "cols": 60,
          "rows": 3,
        }
      ),
    }

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

    class Meta:
        model = CustomUser
        fields = ['name', 'org', 'emails_enabled']