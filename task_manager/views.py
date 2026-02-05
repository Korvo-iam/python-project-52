from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = "home.html"

from django.http import HttpResponse

def test_rollbar_error(request):
    1 / 0  # искусственная ошибка для проверки Rollbar
    return HttpResponse("This won't run")
