from django.conf.urls import url, include
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='home', permanent=False)),
    url(r'^home/$', views.HomeView.as_view(), name='home'),
    url(r'^home/(?P<pk>[0-9]+)/$', views.ChecklistView.as_view(), name='checklist_detail'),
    url(r'^login/$', views.authenticate, name='login'),
    url(r"^logout/$", views.user_logout, name='logout'),
]
