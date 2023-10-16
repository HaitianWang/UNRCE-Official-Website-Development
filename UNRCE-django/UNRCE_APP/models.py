from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager



class SDGEnum(models.TextChoices):   # Using TextChoices to create Enum
    GOAL_1 = 'goal_1', "End poverty in all its forms everywhere"
    GOAL_2 = 'goal_2',"End hunger, achieve food security and improved nutrition and promote sustainable agriculture"
    GOAL_3 = 'goal_3',"Ensure healthy lives and promote well-being for all at all ages"
    GOAL_4 = 'goal_4', "Ensure inclusive and equitable quality education and promote lifelong learning opportunities for all"
    GOAL_5 = 'goal_5', "Achieve gender equality and empower all women and girls"
    GOAL_6 = 'goal_6',"Ensure availability and sustainable management of water and sanitation for all"
    GOAL_7 = 'goal_7', "Ensure access to affordable, reliable, sustainable and modern energy for all"
    GOAL_8 = 'goal_8',"Promote sustained, inclusive and sustainable economic growth, full and productive employment and decent work for all"
    GOAL_9 = 'goal_9',"Build resilient infrastructure, promote inclusive and sustainable industrialization and foster innovation"
    GOAL_10 = 'goal_10',"Reduce inequality within and among countries"
    GOAL_11= 'goal_11',"Make cities and human settlements inclusive, safe, resilient and sustainable"
    GOAL_12 = 'goal_12',"Ensure sustainable consumption and production patterns"
    GOAL_13 = 'goal_13',"Take urgent action to combat climate change and its impacts"
    GOAL_14 = 'goal_14',"Conserve and sustainably use the oceans, seas and marine resources for sustainable development"
    GOAL_15 = 'goal_15',"Protect, restore and promote sustainable use of terrestrial ecosystems, sustainably manage forests, combat desertification, and halt and reverse land degradation and halt biodiversity loss"
    GOAL_16= 'goal_16',"Promote peaceful and inclusive societies for sustainable development, provide access to justice for all and build effective, accountable and inclusive institutions at all levels"
    GOAL_17 = 'goal_17',"Strengthen the means of implementation and revitalize the Global Partnership for Sustainable Development"


class SDG(models.Model):
    sdg = models.CharField(max_length=10, choices=SDGEnum.choices)
    description = models.TextField(null=True)
    def __str__(self):
        return self.title
    



class RCEHub(models.Model):
    hub_name = models.CharField(max_length=255)
    contact_info = models.TextField()
    location = models.CharField(max_length=255, null=True, blank=True)


    
    
    
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
    name = models.CharField(max_length=255, default="", blank=True)
    email_confirmed = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    user_name = models.CharField(max_length=150)  

    # Org field that Ryan made
    org = models.CharField(max_length=255, default="", blank=True)

    # Email field that Ryan made
    emails_enabled = models.BooleanField(default=True)

    interested_projects = models.ManyToManyField('Project', blank=True, related_name="users_interested")
    interested_sdgs = models.ManyToManyField(SDG, related_name='interested_users')
    organisation = models.ForeignKey('Organisation', on_delete=models.SET_NULL, null=True, blank=True)
    role_organisation = models.CharField(max_length=150, default="", blank=True)
    rce_hub = models.ForeignKey(RCEHub, on_delete=models.SET_NULL, null=True, blank=True)   # Not using this one, idk how to use it
    RCE_HUB_CHOICES = [
        ('Great Southern', 'Great Southern'),
        ('Perth Metro', 'Perth Metro')
    ]    
    rce_hub2 = models.CharField(max_length=255, choices=RCE_HUB_CHOICES, default="", blank=True)
    
    
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
    project_cover_image = models.OneToOneField('ProjectImage', on_delete=models.SET_NULL, null=True, blank=True)


    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image<{self.id}> for Project<{self.project_id}>"

class Project(models.Model):
    # choices for fields
    AUDIENCE_CHOICES = [
        ('general', 'General public (any age)'),
        ('adults', 'Adults'),
        ('tertiary', 'Tertiary students'),
        ('high_school', 'High school age'),
        ('primary_school', 'Primary School age'),
        ('early_years', 'Early years'),
        ('adults_60', 'Adults >60'),
        ('other', 'Other'),
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


    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='owned_projects', 
        null=True
    )
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

    audience = models.CharField(max_length=50, choices=AUDIENCE_CHOICES, default=FREQUENCY_CHOICES[0])
    delivery_frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default=FREQUENCY_CHOICES[0])
    language = models.TextField()
    format = models.TextField()
    web_link = models.URLField()
    policy_link = models.URLField()


    
    results = models.TextField(max_length=150, blank=True)
    lessons_learned = models.TextField(max_length=300, blank=True)
    key_messages = models.CharField(max_length=50, blank=True)
    relationship_to_rce_activities = models.TextField(blank=True)
    funding = models.TextField(blank=True)

    sdgs = models.ManyToManyField('SDG', through='ProjectSDG')
    
    main_organisation = models.ForeignKey('Organisation', on_delete=models.SET_NULL, null=True, blank=True, related_name='projects')
    contributing_organizations = models.ManyToManyField('Organisation', related_name='contributing_projects')
    rce_hub = models.ForeignKey(RCEHub, on_delete=models.SET_NULL, null=True, blank=True)  # New RCEHub field



    priority_areas = models.ManyToManyField('PriorityArea', through='ProjectPriorityArea')

    esds = models.ManyToManyField('ESD', through ="ProjectESD")
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    
    APPROVAL_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    ]

    approval = models.CharField(
        max_length=8,
        choices=APPROVAL_CHOICES,
        default=PENDING,
    )
    
    status = models.CharField(max_length=20, choices=[('draft', 'Draft'), ('submitted', 'Submitted')], default='draft')

    

    def __str__(self):
        return self.title



class Follow(models.Model):
    followed_project = models.ForeignKey('Project', on_delete=models.CASCADE)
    following_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class PriorityAccessEnum(models.TextChoices):
    PAA1 = 'priority_area_1', "Priority Action Area 1 - Advancing policy Direct"    
    PAA2 = 'priority_area_2', "Priority Action Area 2 - Transforming learning and training environments Direct"    
    PAA3 = 'priority_area_3', "Priority Action Area 3 - Developing capacities of educators and trainers Direct"
    PAA4 = 'priority_area_4', "Priority Action Area 4 - Mobilizing youth Direct"    
    PAA5 = 'priority_area_5', "Priority Action Area 5 - Accelerating sustainable solutions at local level Direct"

class ESDEnum(models.TextChoices):
    ESD_1 = 'disaster_risk_reduction', "Disaster Risk Reduction"
    ESD_2 = 'traditional_knowledge', "Traditional Knowledge"
    ESD_3 = 'agriculture', "Agriculture"
    ESD_4 = 'arts', "Arts"
    ESD_5 = 'curriculum_development', "Curriculum Development"
    ESD_6 = 'ecotourism', "Ecotourism"
    ESD_7 = 'forests_trees', "Forests & Trees"
    ESD_8 = 'plants_animals', "Plants & Animals"
    ESD_9 = 'waste', "Waste"




class ProjectSDG(models.Model):
    RELATIONSHIP_CHOICES = [
        ('direct', 'Direct'),
        ('indirect', 'Indirect'),
    ]

    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    goal = models.ForeignKey('SDG', on_delete=models.CASCADE)
    relationship_type = models.CharField(max_length=10, choices=RELATIONSHIP_CHOICES)

    class Meta:
        unique_together = ['project', 'goal']


class ESD(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    

class ProjectESD(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    esd = models.ForeignKey('ESD', on_delete=models.CASCADE)
    relationship_type = models.CharField(max_length=10, choices=[('direct', 'Direct'), ('indirect', 'Indirect')])

    class Meta:
        unique_together = ['project', 'esd']
        


class PriorityArea(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    

class ProjectPriorityArea(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    priority_area = models.ForeignKey('PriorityArea', on_delete=models.CASCADE)
    relationship_type = models.CharField(max_length=10, choices=[('direct', 'Direct'), ('indirect', 'Indirect')])

    class Meta:
        unique_together = ['project', 'priority_area']





class Organisation(models.Model):
   # hub = models.ForeignKey('RCEHub', on_delete=models.CASCADE)
    org_name = models.CharField(max_length=255, unique=True)
   # address = models.TextField(null=True, blank=True)
    website_url = models.URLField(null=True, blank=True)
    contact_info = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='organisation_images/', null=True, blank=True)
    
    def __str__(self):
        return self.org_name

