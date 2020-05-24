# Generated by Django 2.2.10 on 2020-05-24 15:12

from django.db import migrations

def set_studygroup_name_from_course_title(apps, schema_editor):
    StudyGroup = apps.get_model('studygroups', 'StudyGroup')
    Course = apps.get_model('studygroups', 'Course')

    for sg in StudyGroup.objects.all():
        empty_values = ['', None]
        if sg.name in empty_values:
            course = Course.objects.get(pk=int(sg.course)), None
            if course is None:
                print("Studygroup {} uses a course that no longer exists: {}".format(sg.id, sg.course))
                sg.name = 'Untitled'

            sg.name = course.title
            sg.save()


class Migration(migrations.Migration):

    dependencies = [
        ('studygroups', '0127_auto_20200524_1508'),
    ]

    operations = [
      migrations.RunPython(set_studygroup_name_from_course_title)
    ]
