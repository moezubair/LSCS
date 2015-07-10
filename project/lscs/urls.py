from django.conf.urls import url, include
from lscs import views

urlpatterns = [
    url(r'^login/', views.authenticate, name='login'),
]
