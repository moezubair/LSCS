import django
from django.contrib.auth.models import User, Group
from lscs.models import Checklist, ChecklistItemSelection, ChecklistItem

# Simple script to insert a test checklist
# Attempts to create a test manager and surveyor user to fulfill the 'created_by' and 'assigned_to' fields



def main():

    django.setup()

    # Create/load surveyor group
    try:
        surveyor = Group.objects.get(name="Surveyor")
    except Group.DoesNotExist:
        surveyor = Group()
        surveyor.name = "Surveyor"
        surveyor.save()

    # Create/load manager group
    try:
        manager = Group.objects.get(name="Manager")
    except Group.DoesNotExist:
        manager = Group()
        manager.name = "Manager"
        manager.save()

    # Create/load users
    test_manager = create_user('testmanager', 'test', 'Test', 'Manager', manager)
    test_surveyor = create_user('testsurveyor', 'test', 'Test', 'Surveyor', surveyor)

    test_checklist = Checklist(
        title='Test Checklist',
        description='this is a test checklist',
        file_number=123,
        land_district='land district test',
        latitude=1.23,
        longitude=1.23,
        status=Checklist.COMPLETED,
        created_by=test_manager,
        assigned_to=test_surveyor
    )

    # Add the groups

    test_checklist.save()

    test_checklistitemselection = create_checklistitemselection(1, test_checklist, test_manager)
    test_checklistitemselection = create_checklistitemselection(1, test_checklist, test_manager)

def create_user(username, password, first_name, last_name, group):

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User()
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.save()

    user.groups.add(group)

    return user

def create_checklistitemselection(selection, checklist, created_by):
    checklistitemselection = ChecklistItemSelection()
    checklistitemselection.selection = selection
    checklistitemselection.checklist = checklist
    checklistitemselection.checklistItem = ChecklistItem.objects.first()
    checklistitemselection.created_by = created_by
    checklistitemselection.save()

    return checklistitemselection

if __name__ == '__main__':
    main()
