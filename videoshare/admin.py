from django.contrib import admin


from .models import User, VideoUpload, Like, UserViewHistory, Comment
# Register your models here.


admin.site.register(User)
admin.site.register(VideoUpload)
admin.site.register(Like)
admin.site.register(UserViewHistory)
admin.site.register(Comment)
