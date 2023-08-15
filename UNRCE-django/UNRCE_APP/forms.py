from django import forms

from .models import Image


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