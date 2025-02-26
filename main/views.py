from django.http import HttpResponse
from django.template import loader

def home(request):
    template = loader.get_template('main/home.html')
    return HttpResponse(template.render({'page': 'home'}, request))