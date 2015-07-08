from django.contrib.auth.models import User
from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Checklist(BaseModel):

    IN_PROGRESS = 1
    UNDER_REVIEW = 2
    COMPLETED = 3

    STATUS_TYPES = (
        (IN_PROGRESS, 'In Progress'),
        (UNDER_REVIEW, 'Under Review'),
        (COMPLETED, 'Completed'),
    )

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    file_number = models.CharField(max_length=30)
    land_district = models.CharField(max_length=50)
    latitude = models.DecimalField (max_digits=8, decimal_places=3)
    longitude = models.DecimalField (max_digits=8, decimal_places=3)
    status = models.IntegerField(choices=STATUS_TYPES)
    created_by = models.ForeignKey(User, related_name='checklistsCreated')
    assigned_to = models.ForeignKey(User, related_name='checklistsAssigned')

class ChecklistItem(models.Model):
    description = models.CharField(max_length=500)

class ChecklistItemSelection(BaseModel):

    UNANSWERED = 1
    YES = 2
    NOT_APPLICABLE = 3

    SELECTION_TYPES = (
        (UNANSWERED, 'Unanswered'),
        (YES, 'Yes'),
        (NOT_APPLICABLE, 'N/A'),
    )

    selection = models.IntegerField(choices=SELECTION_TYPES)
    checklist = models.ForeignKey(Checklist, related_name='itemSelections')
    checklistItem = models.ForeignKey(ChecklistItem)
    created_by = models.ForeignKey(User)

class ChecklistComment(models.Model):
    text = models.TextField()
    checklist = models.ForeignKey(Checklist, related_name='comments')
    created_by = models.ForeignKey(User)