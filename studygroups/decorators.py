from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from studygroups.models import StudyGroup

# Check if user
def user_is_group_facilitator(func):
    def decorated(*args, **kwargs):
        study_group_id = kwargs.get('study_group_id')
        study_group = get_object_or_404(StudyGroup, pk=study_group_id)

        if args[0].user.is_staff or args[0].user == study_group.facilitator:
            return func(*args, **kwargs)
        raise PermissionDenied
    return decorated

