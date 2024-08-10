from django.shortcuts import redirect, render
from .servise import create_user, get_user
from django.views import View
from django.contrib.auth import login, authenticate


class AuthView(View):
    def post(self, request):
        user = authenticate(
            username=request.POST.get("name"), password=request.POST.get("password")
        )
        if get_user(request):
            login(request, get_user(request))
            return redirect("catalog")
        else:
            user = create_user(request)
            login(request, user)
            return redirect("catalog")

    def get(self, request):
        return render(request, "registry/register.html")
