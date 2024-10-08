import json
from django.shortcuts import redirect, render, get_object_or_404
from django.http import Http404, HttpResponseNotFound, HttpResponse, JsonResponse
from .servise import CrudUser
from django.views import View
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .form import UserProfileForm, UserRegisterForm, UserLoginForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


# Для регистрации пользователя
class RegisterUser(View):
    def post(self, request):
        errors = ""
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            params = form.clean()
            res = CrudUser.create_user(**params)
            if res == True:
                if CrudUser.get_user(request=request, **params):
                    return redirect("home:base")
                else:
                    errors += "Системная ошибка попробуйте позже"
            else:
                errors += res
        else:
            errors += "Ошибка валидации полей: " + ", ".join(
                [
                    f"{field}: {', '.join(error_list)}"
                    for field, error_list in form.errors.items()
                ]
            )
        return render(
            request,
            "registry/register.html",
            {"form": form, "error": errors},
        )

    def get(
        self,
        request,
    ):
        if not request.user.is_authenticated:
            return render(
                request,
                "registry/register.html",
                {
                    "form": UserRegisterForm(),
                },
            )
        else:
            return HttpResponseNotFound()


class LoginUser(View):
    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            res = CrudUser.get_user(request=request, **form.clean())
            if res:
                return redirect("home:base")
            else:
                return render(
                    request,
                    "registry/login.html",
                    {
                        "email": request.POST.get("email"),
                        "error": "Неверные логин или пароль",
                    },
                )
        return render(
            request,
            "registry/login.html",
            {
                "email": request.POST.get("email"),
                "error": form.errors.as_text(),
            },
        )

    def get(self, request):
        if request.user.is_authenticated:
            CrudUser.logout_user(request)
            return redirect("home:base")
        return render(request, "registry/login.html", {"form": UserLoginForm()})

    def put(self, request):
        pass

    def delete(self, request):
        pass

    def update(self, request):
        pass


@method_decorator(login_required, name="dispatch")
class UserProfile(View):
    def get(self, request):
        form = UserProfileForm()
        return render(
            request,
            "registry/profile.html",
            {"user": request.user, "form": form},
        )

    def post(self, request):
        pass

    def delete(self, request):
        CrudUser.delete_user(request)
        return redirect("home:base")

    def put(self, request):
        # Парсим данные из request.body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

        # Передаем данные в форму
        form = UserProfileForm(data)
        if form.is_valid():
            data = form.clean()
            res = CrudUser.update_user(request, **data)
            if res == True:
                return JsonResponse({"status": "success"})
            else:
                # Если обновление не удалось, перенаправляем на предыдущую страницу
                return JsonResponse({"status": "error", "error": res})
        else:
            # В случае невалидной формы также перенаправляем на предыдущую страницу с ошибками
            return JsonResponse({"status": "error", "error": form.errors.as_text()})
