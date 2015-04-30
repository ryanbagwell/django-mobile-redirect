from django.conf import settings
from django.conf.urls import patterns, include, url
from django.http import HttpResponse

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()



def test_view(request):
    return HttpResponse("You shouldn't see this if it's a mobile device.")

urlpatterns = patterns('',
    url(r'^', test_view),
)
