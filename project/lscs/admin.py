from django.contrib import admin
from lscs.models import Checklist, ChecklistItem, ChecklistComment

admin.site.register(Checklist)
admin.site.register(ChecklistItem)
admin.site.register(ChecklistComment)
# Register your models here.
