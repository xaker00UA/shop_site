from django.shortcuts import render


# Create your views here.
def base(request):
    if not request.session.session_key:
        request.session.create()
    return render(request, "html/base.html")
