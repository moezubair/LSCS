from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.forms import model_to_dict, fields_for_model
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.http import require_http_methods

from project import settings
from .models import Checklist
from .forms import ChecklistForm


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


@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)


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

    # Restrict access to this view to logged in users:
    #     https://docs.djangoproject.com/en/1.8/topics/class-based-views/intro/#decorating-the-class
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)


class ChecklistView(generic.FormView):
    template_name = 'checklist_detail.html'
    form_class = ChecklistForm
    success_url = 'home'

    # customize the context object that is passed to the template
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ChecklistView, self).get_context_data(**kwargs)

        # get the instance of the form being processed
        form = self.get_form(ChecklistForm)

        # Set the field to be readonly
        ''' TODO:
            Set fields to be readonly based on the status of the checklist being updated and the type of user (surveyor or manager) '''

        form.fields['title'].widget.attrs['readonly'] = True

        # Update the context object
        context['form'] = form
        return context

    # once the form is validated, save it (which in turn saves the new/updated model to the db)
    def form_valid(self, form):
        form.save()
        return super(ChecklistView, self).form_valid(form)

