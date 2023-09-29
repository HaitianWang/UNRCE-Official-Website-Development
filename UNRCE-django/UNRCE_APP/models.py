from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class Image(models.Model):
  # image title, not blank string with maximum of 60 characters
  title = models.CharField(max_length=60, blank=False)

  # the uploaded image. It is important to understand that
  # django will not store the image in the database.
  # The image field in the database table will contain the
  # image name (with max_length = 36) whereas the actual image
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

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class ProjectFile(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    file = models.FileField(upload_to='project_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File<{self.id}> for Project<{self.project_id}>"
    

class ProjectImage(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image<{self.id}> for Project<{self.project_id}>"
    

class Project(models.Model):
    # choices for fields
    AUDIENCE_CHOICES = [
        ('general', 'General public (any age)'),
        ('target', 'Particular target Audience (Please specify)'),
        ('adults', 'Adults'),
        ('tertiary', 'Tertiary students'),
        ('high_school', 'High school age'),
        ('primary_school', 'Primary School age'),
        ('early_years', 'Early years'),
        ('adults_60', 'Adults >60 please'),
    ]
    FREQUENCY_CHOICES = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('biannually', 'Biannually'),
        ('annually', 'Annually'),
        ('ongoing', 'Ongoing'),
        ('once', 'Once'),
        ('irregular', 'Opportunistic/Irregularly'),
        ('on_demand', 'Permanent/On demand'),
    ]

    SELECTION_CHOICES = [
        ('direct', 'Direct'),
        ('indirect', 'Indirect'),
    ]


    
    title = models.TextField(default="Default Title")


    #manager = models.ForeignKey(	
       # settings.AUTH_USER_MODEL,	
      #  on_delete=models.CASCADE,	
     #   default=1	
    #)


    project_cover_image = models.FileField(upload_to='project_images/', null=True, blank=True)


    description = models.TextField()


    created_at = models.DateTimeField(auto_now_add=True)  # Set to 'now' when the record is created
    concluded_on = models.DateTimeField(null=True, blank=True)  # Null by default

    files = models.ManyToManyField('ProjectFile', related_name='projects')
    images = models.ManyToManyField('ProjectImage', related_name='projects')


    
    audience = models.CharField(max_length=50, choices=AUDIENCE_CHOICES)
    delivery_frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    language = models.TextField()
    format = models.TextField()
    web_link = models.TextField()
    policy_link = models.TextField()

    
    results = models.TextField(max_length=150, blank=True)
    lessons_learned = models.TextField(max_length=100, blank=True)
    key_messages = models.CharField(max_length=50, blank=True)
    relationship_to_rce_activities = models.TextField(blank=True)
    funding = models.TextField(blank=True)

    sdgs = models.ManyToManyField('SDG', through='ProjectSDG')
    contributing_organizations = models.ManyToManyField('Organisation', related_name='contributing_projects')
    affiliations = models.ManyToManyField('Organisation', related_name='affiliated_projects')


    priority_area_1 = models.CharField(max_length=10, choices=SELECTION_CHOICES, default='', blank=True)
    priority_area_2 = models.CharField(max_length=10, choices=SELECTION_CHOICES, default='', blank=True)
    priority_area_3 = models.CharField(max_length=10, choices=SELECTION_CHOICES, default='', blank=True)
    priority_area_4 = models.CharField(max_length=10, choices=SELECTION_CHOICES, default='', blank=True)
    priority_area_5 = models.CharField(max_length=10, choices=SELECTION_CHOICES, default='', blank=True)


    disaster_risk_reduction = models.CharField(max_length=10, choices=SELECTION_CHOICES, default='', blank=True)
    traditional_knowledge = models.CharField(max_length=10, choices=SELECTION_CHOICES, default='', blank=True)
    agriculture = models.CharField(max_length=10, choices=SELECTION_CHOICES, default='', blank=True)
    arts = models.CharField(max_length=10, choices=SELECTION_CHOICES, default='', blank=True)
    curriculum_development = models.CharField(max_length=10, choices=SELECTION_CHOICES, default='', blank=True)
    ecotourism = models.CharField(max_length=10, choices=SELECTION_CHOICES, default='', blank=True)
    forests_trees = models.CharField(max_length=10, choices=SELECTION_CHOICES, default='', blank=True)
    plants_animals = models.CharField(max_length=10, choices=SELECTION_CHOICES, default='', blank=True)
    waste = models.CharField(max_length=10, choices=SELECTION_CHOICES, default='', blank=True)


    

    def __str__(self) -> str:
        return f"Project<{self.id}>"



class Follow(models.Model):
    followed_project = models.ForeignKey('Project', on_delete=models.CASCADE)
    following_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class SDGEnum(models.TextChoices):   # Using TextChoices to create Enum
    GOAL_1 = 'goal_1'
    GOAL_2 = 'goal_2'
    GOAL_3 = 'goal_3'
    GOAL_4 = 'goal_4'
    GOAL_5 = 'goal_5'
    GOAL_6 = 'goal_6'
    GOAL_7 = 'goal_7'
    GOAL_8 = 'goal_8'
    GOAL_9 = 'goal_9'
    GOAL_10 = 'goal_10'
    GOAL_11= 'goal_11'
    GOAL_12 = 'goal_12'
    GOAL_13 = 'goal_13'
    GOAL_14 = 'goal_14'
    GOAL_15 = 'goal_15'
    GOAL_16= 'goal_16'
    GOAL_17 = 'goal_17'

class SDG(models.Model):
    sdg = models.CharField(max_length=10, choices=SDGEnum.choices)

class ProjectSDG(models.Model):
    SELECTION_CHOICES = [
        ('direct', 'Direct'),
        ('indirect', 'Indirect'),
    ]
    
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    sdg = models.ForeignKey('SDG', on_delete=models.CASCADE)
    relationship_type = models.CharField(max_length=10, choices=SELECTION_CHOICES, default='')

    class Meta:
        unique_together = ['project', 'sdg']


class RCEHub(models.Model):
    hub_name = models.CharField(max_length=255)
    contact_info = models.TextField()

class Organisation(models.Model):
    hub = models.ForeignKey('RCEHub', on_delete=models.CASCADE)
    org_name = models.CharField(max_length=255, unique=True)
    address = models.TextField(null=True, blank=True)

#Model view for Institutions
# class Institution(models.Model):
#     name = models.CharField(max_length=255)
#     link = models.URLField()
#     image = models.ImageField(upload_to='images_organisations/')

"""	
class Affiliation(models.Model):	
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)	
    org = models.ForeignKey('Organisation', on_delete=models.CASCADE)	
    authenticated = models.BooleanField(default=False)	
    #authenticated_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name="authenticated_affiliations", verbose_name="Authenticated by")	
    #authentication_timestamp = models.DateTimeField(null=True, blank=True, verbose_name="Authentication Timestamp")	
class ProjectPartnerCompanies(models.Model):	
    project = models.ForeignKey('Project', on_delete=models.CASCADE)	
    partner_company = models.ForeignKey('Organisation', on_delete=models.CASCADE)	
    class Meta:	
        unique_together = ['project', 'partner_company']	
"""