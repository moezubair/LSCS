from django.contrib import admin
from lscs.models import Checklist, ChecklistItem, ChecklistComment, ChecklistItemGroup, ChecklistItemSelection


admin.site.register(Checklist)
admin.site.register(ChecklistItem)
admin.site.register(ChecklistComment)
admin.site.register(ChecklistItemGroup)
admin.site.register(ChecklistItemSelection)
# Register your models here.
