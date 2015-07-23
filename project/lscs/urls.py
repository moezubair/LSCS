from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.views.generic import RedirectView
admin.autodiscover()
urlpatterns = [
    url(r'^$', RedirectView.as_view(url='home', permanent=False)),
    url(r'^home/$', views.HomeView.as_view(), name='home'),
    url(r'^home/(?P<pk>[0-9]+)/$', views.EditChecklistView.as_view(), name='checklist_detail'),
    url(r'^login/$', views.authenticate, name='login'),
    url(r"^logout/$", views.user_logout, name='logout'),
    url(r"^admin/", include(admin.site.urls)),
    url(r'^create_checklist/$', views.CreateChecklistView.as_view(), name='create_checklist'),
]
