from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.views.decorators.http import require_http_methods

from project import settings
from .models import Checklist


@require_http_methods(["GET", "POST"])
def authenticate(request):

    if request.method == 'POST':

        auth_form = AuthenticationForm(request=request, data=request.POST)

        if auth_form.is_valid():

            login(request, auth_form.get_user())

            next_url = request.POST['next']

            if next_url:
                return HttpResponseRedirect(next_url)
            else:
                return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

    else:

        auth_form = AuthenticationForm()

    return render(request, 'login.html', {'form': auth_form})


class HomeView(generic.ListView):
    template_name = 'home.html'
    context_object_name = 'user_checklist_list'

    def get_queryset(self):
        # get reference to the user accessing the view
        user = self.request.user

        # get the set of checklists created by this user or assigned to this user
        user_checklists = Checklist.objects.all().filter(Q(created_by=user) | Q(assigned_to=user))

        # sort the set by date updated most recently
        sorted_list = sorted(user_checklists, key=lambda checklist: checklist.updated_at, reverse=True)
        return sorted_list

