from django.contrib.auth.models import User
from lscs.models import Checklist

# Simple script to insert a test checklist
# Attempts to create a test manager and surveyor user to fulfill the 'created_by' and 'assigned_to' fields
def main():
    test_manager = find_first_matching_user('testmanager', 'test')
    test_surveyor = find_first_matching_user('testsurveyor', 'test')

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
    test_checklist.save()

def find_first_matching_user(username,password):
    matching_users = list(User.objects.filter(username=username)[:1])

    if not matching_users:
        test_user = User()
        test_user.username = username
        test_user.set_password(password)
        test_user.save()
        return test_user
    else:
        return matching_users[0]

if __name__ == '__main__':
    main()
