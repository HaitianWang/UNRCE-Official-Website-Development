# Generated by Django 4.2.4 on 2023-10-15 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UNRCE_APP', '0009_customuser_email_confirmed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='audience',
            field=models.CharField(choices=[('general', 'General public (any age)'), ('adults', 'Adults'), ('tertiary', 'Tertiary students'), ('high_school', 'High school age'), ('primary_school', 'Primary School age'), ('early_years', 'Early years'), ('adults_60', 'Adults >60'), ('other', 'Other')], max_length=50),
        ),
    ]
