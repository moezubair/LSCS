from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Checklist, ChecklistItem, ChecklistItemSelection


class EditChecklistForm(ModelForm):
    def __init__(self, *args, **kwargs):
        # Call the super constructor
        super(EditChecklistForm, self).__init__(*args, **kwargs)

        # Change assigned_to to only show surveyors
        self.fields['assigned_to'].queryset = User.objects.filter(groups__name="Surveyor")

    class Meta:
        model = Checklist
        fields = ['title', 'description', 'file_number', 'land_district', 'latitude', 'longitude', 'status', 'assigned_to']


class CreateChecklistForm(ModelForm):
    def __init__(self, *args, **kwargs):
        # Call the super constructor
        super(CreateChecklistForm, self).__init__(*args, **kwargs)

        # Change assigned_to to only show surveyors
        self.fields['assigned_to'].queryset = User.objects.filter(groups__name="Surveyor")

    class Meta:
        model = Checklist
        fields = ['title', 'description', 'file_number', 'land_district', 'latitude', 'longitude', 'assigned_to']


class ChecklistItemSelectionForm(ModelForm):

    selection = forms.ChoiceField(choices=ChecklistItemSelection.SELECTION_TYPES, widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):

        # Call the super constructor
        super(ChecklistItemSelectionForm, self).__init__(*args, **kwargs)

        current_selection = self.instance

        try:
            checklist_item = ChecklistItem.objects.get(pk=current_selection.checklistItem.pk)
            item_description = str(checklist_item.description)
        except Exception:
            item_description = "Description Not Found"

        self.fields['selection'].label = item_description
        # self.fields['selection'].empty_label = None

    class Meta:
        model = ChecklistItemSelection
        fields = ['checklistItem', 'selection']
        widgets = {
            'checklistItem': forms.HiddenInput()
        }
