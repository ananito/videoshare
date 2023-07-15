import random
import shutil
import tempfile
import string

import ffmpeg
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views import View

from .models import VideoUpload


class VideoUploadView(View):
    def get(self, request):
        return HttpResponseRedirect(reverse("index"))

    def post(self, request):
        video = request.FILES.get("videoFile")
        thumbnail = request.FILES.get("videoThumbnail")
        title = request.POST.get("videoTitle")
        description = request.POST.get("videoDescription")
        private = request.POST.get("videoPrivate")

        if title == "":
            return JsonResponse(
                {"status": "error", "message": "Invalid title. Please input a title!"},
                status=400,
            )

        # Validate uploaded file
        if not self.is_valid_video_file(video):
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Invalid video file. Video file should be an mp4!",
                },
                status=422,
            )

        if private == "True":
            private = True
        else:
            private = False

        # Generate video_id
        video_id = self.generate_video_id()

        if thumbnail:
            # Thumbnail provided by the user
            file_obj = VideoUpload(
                user=request.user,
                title=title,
                description=description,
                video=video,
                private=private,
                video_id=video_id,
                thumbnail=thumbnail,
            )
        else:
            # Generate thumbnail using FFmpeg
            file_obj = VideoUpload(
                user=request.user,
                title=title,
                description=description,
                video=video,
                video_id=video_id,
                private=private,
            )
            file_obj.save()

            thumbnail_path = self.generate_thumbnail(file_obj.video.path)[1]
            destination = f"media/uploads/images/{file_obj.unique_id}.jpeg"
            shutil.move(thumbnail_path, destination)
            destination = f"uploads/images/{file_obj.unique_id}.jpeg"
            file_obj.thumbnail.name = destination
            file_obj.save()
        file_obj.save()

        return JsonResponse(
            {"status": "success", "message": "File uploaded successfully."}, status=200
        )

    # Generate video id of length 8
    def generate_video_id(self):
        letters = string.ascii_letters + string.digits + "_-"
        video_id = "".join(random.SystemRandom().choice(letters) for i in range(8))

        exists = VideoUpload.objects.filter(video_id=video_id).exists()

        if exists:
            return self.generate_video_id()
        return video_id

    # Checking video type
    def is_valid_video_file(self, video):
        # Check if the file has a valid video MIME type
        valid_mime_types = ["video/mp4", "video/mpeg"]
        return video.content_type in valid_mime_types

    # Thumbnail generation at random time
    def generate_thumbnail(self, video):
        # Get the video duration using ffprobe
        duration = float(ffmpeg.probe(video)["format"]["duration"])

        # Generate a random time
        time = random.randint(0, int(duration))

        # Create a temp file for the thumbnail
        temp = tempfile.mkstemp(suffix=".jpeg", dir="media/uploads/images/")

        try:
            # Generate thumbnail using FFmpeg
            ffmpeg.input(video, ss=str(time)).output(
                temp[1], vframes=1
            ).overwrite_output().run(capture_stdout=True, capture_stderr=True)

            return temp
        except ffmpeg.error:
            return JsonResponse(
                {"status": "error", "message": "Thumbnail Generation fail!"}, status=400
            )
