import os
import django

from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas

# Initialize Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'UNRCE.settings')
django.setup()

from UNRCE_APP.models import Project

# Function to get the first project from the Django model
def get_data_from_db():
    return Project.objects.first()

# Function to generate PDF displaying all details of the project
def generate_pdf(project):
    c = canvas.Canvas("output.pdf", pagesize=landscape(letter))
    width, height = landscape(letter)
    
    x = 50  # start x position
    y = height - 50  # start y position
    
    for field in Project._meta.fields:  # Loop through all fields of the Project model
        field_name = field.name
        field_value = getattr(project, field_name)  # Dynamically get the value of the current field for the project
        
        c.drawString(x, y, f"{field_name}: {field_value}")  # Display field name and its value
        y -= 20  # Move to the next line after displaying each field
        if y < 50:  # Simple check to prevent writing below page margins
            c.showPage()
            y = height - 50  # reset the Y position
            x = 50   # reset the X position
    
    c.save()

# Get the project and generate the PDF
project = get_data_from_db()
generate_pdf(project)
