from django.contrib.auth.views import LogoutView


class LogoutView(LogoutView):
    template_name = "core/registration/login.html"
