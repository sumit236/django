from django.urls import path
from . import view


urlpatterns = [
    path('', view.homepage, name='home'),
    path('counts/', view.counts, name='count'),
    path('about/', view.about, name='about'),
]
