from django.shortcuts import redirect
from django.views import View


class ProfileUpdateView(View):
    """Views para atualizar os dados do perfil do usuario"""

    def post(self, request, *args, **kwargs):
        try:
            data = request.POST
            request.user.first_name = data.get("first_name")
            request.user.last_name = data.get("last_name")
            request.user.email = data.get("email")
            request.user.save()

        except Exception as error:
            print(error)

        return redirect("core:profile")  # Redirect using name url parameter
