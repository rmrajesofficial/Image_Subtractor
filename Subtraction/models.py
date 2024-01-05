from django.db import models

# Create your models here.
class ProjectDocument(models.Model):
    file = models.FileField(upload_to='documents/',blank=False)