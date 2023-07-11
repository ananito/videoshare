import random
import shutil
import tempfile
import threading

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

        if thumbnail:
            # Thumbnail provided by the user
            file_obj = VideoUpload(
                user=request.user,
                title=title,
                description=description,
                video=video,
                private=private,
                thumbnail=thumbnail,
            )
        else:
            # Generate thumbnail using FFmpeg
            file_obj = VideoUpload(
                user=request.user,
                title=title,
                description=description,
                video=video,
                private=private,
            )
            file_obj.save()

            thumbnail_path = self.generate_thumbnail(file_obj.video.path)[1]
            destination = f"media/uploads/images/{file_obj.unique_id}.jpeg"
            shutil.move(thumbnail_path, destination)
            file_obj.thumbnail = destination
            file_obj.save()
        file_obj.save()

        # Start a new thread to upload the file
        thread = threading.Thread(target=self.upload_file, args=(file_obj,))
        thread.start()

        return JsonResponse(
            {"status": "success", "message": "File uploaded successfully."}, status=200
        )

    def is_valid_video_file(self, video):
        # Check if the file has a valid video MIME type
        valid_mime_types = ["video/mp4", "video/mpeg"]
        return video.content_type in valid_mime_types

    def generate_thumbnail(self, video):
        temp = tempfile.mkstemp(suffix=".jpeg")
        time = random.randint(1, 10)

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

    def upload_file(self, file_obj):
        file_path = file_obj.video.path
        total_size = file_obj.video.size
        uploaded_size = 0
        progress = 0

        with open(file_path, "wb") as destination:
            for chunk in file_obj.video.chunks():
                destination.write(chunk)
                uploaded_size += len(chunk)
                new_progress = int((uploaded_size / total_size) * 100)

                if new_progress != progress:
                    progress = new_progress
                    # Update progress in the database or use a different storage mechanism
                    file_obj.progress = progress
                    file_obj.save()

        # Upload completed, set progress to 100
        file_obj.progress = 100
        file_obj.save()
