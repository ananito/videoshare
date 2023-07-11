from django.db import models
import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator


# Create your models here.
class User(AbstractUser):
    pass


class VideoUpload(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    video = models.FileField(upload_to="media/uploads/videos/", validators=[FileExtensionValidator(allowed_extensions=['mp4'])])
    thumbnail = models.ImageField(upload_to="media/uploads/images/", blank=True, null=True)
    private = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
