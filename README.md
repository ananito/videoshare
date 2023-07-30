# VideoShare
VideoShare is a videosharing site that allowes users to share video, and interact with the video.

# Components and Functionality

## Auth

- `Login` function created using django's `LoginView`.
- `logout` function created using django's `LogoutView`.
- `Register` function in `views.py`. Built using [`UserRegistrationForm`](#forms) in `form.py` which inherit from django's builtin function `UserCreationForm`.

## Video
- [VideoUploader](./videoshare/fileuploader.py) 

- `index` render the front page of the website. It generates a list of 50 videos to be shown on the page.
- `watch_view` renders the videoupload
# Forms
