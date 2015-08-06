from django.contrib.auth.models import User
from django.forms import ModelForm, BaseFormSet
from .models import Checklist, ChecklistItem, ChecklistItemSelection


class EditChecklistForm(ModelForm):
    def __init__(self, *args, **kwargs):
        # Call the super constructor
        super(EditChecklistForm, self).__init__(*args, **kwargs)

        # Change created_by field to only show managers
        self.fields['created_by'].queryset = User.objects.filter(groups__name="Manager")

        # Change assigned_to to only show surveyors
        self.fields['assigned_to'].queryset = User.objects.filter(groups__name="Surveyor")

    class Meta:
        model = Checklist
        exclude = ['id']

class CreateChecklistForm(ModelForm):
    def __init__(self, *args, **kwargs):
        # Call the super constructor
        super(CreateChecklistForm, self).__init__(*args, **kwargs)

        # Change assigned_to to only show surveyors
        self.fields['assigned_to'].queryset = User.objects.filter(groups__name="Surveyor")

    class Meta:
        model = Checklist
        fields = ['title', 'description', 'file_number', 'land_district', 'latitude', 'longitude', 'assigned_to']


class ChecklistItemForm(ModelForm):

    class Meta:
        model = ChecklistItem
        exclude = ['id']