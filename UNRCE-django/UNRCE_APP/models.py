from django.conf import settings
from django.db import models

class Image(models.Model):
  # image title, not blank string with maximum of 60 characters
  title = models.CharField(max_length=60, blank=False)

  # the uploaded image. It is important to understand that
  # django will not store the image in the database.
  # The image field in the database table will contain the
  # image name (with max_length = 36) whereas the actual image
  # will be stored in the directory defined in giffy/settings.py.
  image = models.ImageField(max_length=36)

  # image upload date and time
  uploaded_date = models.DateTimeField()

  # link to the user that uploaded the image
  uploaded_by = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
  )

  def __str__(self) -> str:
    return f"Image<{self.id}>"