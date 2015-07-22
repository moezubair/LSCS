from django.contrib import admin
from lscs.models import Checklist, ChecklistItem, ChecklistComment, ChecklistItemGroup

admin.site.register(Checklist)
admin.site.register(ChecklistItem)
admin.site.register(ChecklistComment)
admin.site.register(ChecklistItemGroup)
# Register your models here.
