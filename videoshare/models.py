from django.db import models
import uuid

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


# Create your models here.
class User(AbstractUser):
    pass


class VideoUpload(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    video = models.FileField(upload_to="uploads/videos/")
    thumbnail = models.ImageField(upload_to="uploads/images/", blank=True, null=True)
    private = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    video_id = models.CharField(max_length=120, blank=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} uploaded by {self.user.username}"


class Like(models.Model):
    video = models.ForeignKey(VideoUpload, on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name="video_likes", blank=True)
    disliked_by = models.ManyToManyField(User, related_name="video_dislikes", blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.video.title


class UserViewHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    videos = models.ManyToManyField(VideoUpload, blank=True)

    class Meta:
        verbose_name = _("UserViewHistory")
        verbose_name_plural = _("UserViewHistorys")

    def __str__(self):
        return f"{self.user.username}"


class Comment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(blank=False)
    video = models.ForeignKey(VideoUpload, on_delete=models.CASCADE)
    likes = models.IntegerField(blank=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return self.user.username


class CommentLike(models.Model):

    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ManyToManyField("User")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("CommentLike")
        verbose_name_plural = _("CommentLikes")

    def __str__(self):
        return self.comment
