from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from .models import VideoUpload


@method_decorator(login_required, name="dispatch")
class MyVideos(View):
    # Update the video
    def post(self, request):
        try:
            video = VideoUpload.objects.get(
                user=request.user, video_id=request.POST.get("video_id")
            )
            video.title = request.POST.get("videoTitle")
            video.description = request.POST.get("videoDescription")
            if not request.POST.get("videoPrivate"):
                video.private = False
            else:
                video.private = True
            video.save()
        except VideoUpload.DoesNotExist:
            return JsonResponse({"error": "Video does not exists"}, status=404)

        return JsonResponse({"message": "Post was updated successfully"})

    # Delete the video
    def delete(self, request, video_id):
        try:
            video = VideoUpload.objects.get(user=request.user, video_id=video_id)
            video.delete()
        except VideoUpload.DoesNotExist:
            return JsonResponse({"error": "Video does not exists"}, status=404)

        return JsonResponse({"message": "Video was successfully deleted "}, status=200)

    def get(self, request):
        videos = VideoUpload.objects.filter(user=request.user).order_by("-pk")
        return render(request, "my_videos.html", {"videos": videos})
