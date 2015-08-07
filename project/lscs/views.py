import urllib.request
import json

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.http import require_http_methods

from project import settings
from .models import Checklist, ChecklistItem, ChecklistItemSelection
from .forms import EditChecklistForm, CreateChecklistForm, ChecklistItemSelectionForm


def get_user_type(user):

    # We default to surveyor if they are not a manager (for now). Should clean this up to logout user if they are not either
    # Should also clean up user_type to use an enum or constant rather than a string

    if user.groups.filter(name="Manager").count() > 0:
        user_type = "Manager"
    else:
        user_type = "Surveyor"

    return user_type

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

        user_type = get_user_type(user)

        # get the set of checklists created by this user or assigned to this user
        if user_type == "Manager":
            user_checklists = user.checklistsCreated.all()
        else:
            user_checklists = user.checklistsAssigned.all()

        # sort the set by date updated most recently
        sorted_list = sorted(user_checklists, key=lambda checklist: checklist.updated_at, reverse=True)
        return sorted_list

    def post(self, request, *args, **kwargs):

        user_type = get_user_type(request.user)

        # check if a request to delete a checklist was made
        if user_type == "Manager" and 'delete' in request.POST:
            # get the checklist from the POST request and delete it
            checklist_id = request.POST.get('delete')
            checklist = Checklist.objects.get(id=checklist_id)
            checklist.delete()

        # refresh the page regardless
        return HttpResponseRedirect('/home/')


    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super(HomeView, self).get_context_data(**kwargs)

        # get the instance of the form being processed
        #form = self.get_form(HomeView)

        # check if the current user is a manager
        user = self.request.user

        context['user_type'] = get_user_type(user)
        return context

    # Restrict access to this view to logged in users:
    #     https://docs.djangoproject.com/en/1.8/topics/class-based-views/intro/#decorating-the-class
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)


class EditChecklistView(generic.UpdateView):
    template_name = 'checklist_detail.html'
    model = Checklist
    form_class = EditChecklistForm
    success_url = '/home/'

    def get_context_data(self, **kwargs):
        temperature = {}
        # Call the base implementation first to get a context
        context = super(EditChecklistView, self).get_context_data(**kwargs)

        # get the instance of the form being processed
        form = self.get_form(EditChecklistForm)

        # get instance of checklist being updated
        checklist = self.object

        # get the formset of ChecklistItemSelections
        item_form_set = self.get_checklist_item_form_set(checklist)

        # get the current user
        user = self.request.user

        user_type = get_user_type(user)

        # if the user is not a manager, restrict edibility of certain fields
        if user_type != "Manager":
            self.set_fields_readonly(form)
            self.hide_choice_fields(form)

        # Get the Weather
        weatherService = "http://api.openweathermap.org/data/2.5/weather?units=metric&lat=" + str(
            checklist.latitude) + "&lon=" + str(checklist.longitude)

        # Acces weather data from weather service
        weatherStream = urllib.request.urlopen(weatherService)

        try:
            # Read the weather data and parse
            json_result = weatherStream.read()
            parsed_json = json.loads(json_result.decode())
            temperature['min'] = parsed_json['main']['temp_min']
            temperature['max'] = parsed_json['main']['temp_max']
            temperature['humidity'] = parsed_json['main']['humidity']
            temperature['temp'] = parsed_json['main']['temp']
            temperature['pressure'] = parsed_json['main']['pressure']
        except Exception as e:
            temperature = "Weather API Not available" + str(e)

        # Update the context object
        context['user_type'] = user_type
        context['form'] = form
        context['item_form_set'] = item_form_set
        context['weather'] = temperature

        return context

    def get_checklist_item_form_set(self, checklist):

        ChecklistItemFormSet = modelformset_factory(ChecklistItemSelection, fields=['checklistItem', 'selection'],
                                                    form=ChecklistItemSelectionForm)

        selection_queryset = ChecklistItemSelection.objects.filter(checklist=checklist)

        selection_query_results = list(selection_queryset.values())

        form_set = ChecklistItemFormSet(queryset=selection_queryset)

        # remove any forms without a pk (weird bug, where formset generates empty form)
        for form in form_set:
            if form.instance.pk is None:
                form_set.forms.remove(form)

        # make the description field uneditable
        for form in form_set:
            self.set_formsetfields_readonly(form)

        return form_set

    def form_valid(self, form):

        checklist = form.instance

        checklist.save()

        return super(EditChecklistView, self).form_valid(form)

    def set_fields_readonly(self, form):
        checklist_fields = [
            'title',
            'description',
            'file_number',
            'land_district',
            'latitude',
            'longitude',
        ]
        for key, value in form.fields.items():
            for field in checklist_fields:
                if key == field:
                    form.fields[key].widget.attrs['readonly'] = True

    def hide_choice_fields(self, form):
        checklist_choice_fields = [
            'status',
            'created_by',
            'assigned_to',
        ]
        for key, value in form.fields.items():
            for field in checklist_choice_fields:
                if key == field:
                    form.fields[key].widget.attrs['disabled'] = 'disabled'

    def set_formsetfields_readonly(self, form):
        item_selection_fields = [
            'checklistItem',
        ]
        for key, value in form.fields.items():
            for field in item_selection_fields:
                if key == field:
                    form.fields[key].widget.attrs['readonly'] = True

def UpdateChecklistItemsView(request):
    ChecklistItemSelectionFormSet = modelformset_factory(ChecklistItemSelection, form=ChecklistItemSelectionForm, fields=['checklistItem', 'selection'])
    if request.method == 'POST':
        formset = ChecklistItemSelectionFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
    else:
        formset = ChecklistItemSelectionFormSet()
    return HttpResponseRedirect('/home/')

class CreateChecklistView(generic.FormView):

    template_name = 'create_checklist.html'
    form_class = CreateChecklistForm
    success_url = '/home/'

    def form_valid(self, form):

        checklist = form.instance

        checklist.created_by = self.request.user
        checklist.status = Checklist.IN_PROGRESS

        checklist.save()

        checklistItems = ChecklistItem.objects.all()

        for checklistItem in checklistItems:

            checklistItemSelection = ChecklistItemSelection()
            checklistItemSelection.checklist = checklist
            checklistItemSelection.checklistItem = checklistItem
            checklistItemSelection.selection = ChecklistItemSelection.UNANSWERED
            checklistItemSelection.created_by = checklist.assigned_to

            checklistItemSelection.save()

        return super(CreateChecklistView, self).form_valid(form)

    def get(self, request, *args, **kwargs):

        user_type = get_user_type(request.user)

        # Make sure we're a manager
        if user_type == "Manager":
            return super(CreateChecklistView, self).get(request, **kwargs)
        else:
            return HttpResponseRedirect('/home/')

    def post(self, request, *args, **kwargs):

        user_type = get_user_type(request.user)

        # Make sure we're a manager
        if user_type == "Manager":
            return super(CreateChecklistView, self).post(request, **kwargs)
        else:
            return HttpResponseRedirect('/home/')
