from django.conf.urls import url, include
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^home/', views.HomeView.as_view(), name='home'),
    url(r'^login/', views.authenticate, name='login'),
    url(r"^logout/", views.user_logout, name='logout'),
    url(r'^$', RedirectView.as_view(url='home', permanent=False)),
]
