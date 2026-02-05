from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = "home.html"

from django.shortcuts import render
from django.http import HttpResponse

#rollback подключен успешно
#def index(request):
#    a = None
#    a.hello() # Creating an error with an invalid line of code
#    return HttpResponse("Hello, world. You're at the pollapp index.")
