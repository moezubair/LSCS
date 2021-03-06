from django.contrib.auth.models import User, AbstractBaseUser
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
    latitude = models.DecimalField(max_digits=8, decimal_places=3)
    longitude = models.DecimalField(max_digits=8, decimal_places=3)
    status = models.IntegerField(choices=STATUS_TYPES)
    created_by = models.ForeignKey(User, related_name='checklistsCreated')
    assigned_to = models.ForeignKey(User, related_name='checklistsAssigned')

    def __str__(self):
        return self.title

    def get_status(self):
        return [item[1] for item in Checklist.STATUS_TYPES if item[0] == self.status][0]


class ChecklistItemGroup(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class ChecklistItem(models.Model):
    description = models.CharField(max_length=500)
    group = models.ForeignKey(ChecklistItemGroup, related_name='checklistItems')

    def __str__(self):
        return self.description


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
