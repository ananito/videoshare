from django.contrib import admin


from .models import User, VideoUpload, Like
# Register your models here.


admin.site.register(User)
admin.site.register(VideoUpload)
admin.site.register(Like)
