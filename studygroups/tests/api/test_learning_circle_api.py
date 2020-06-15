# coding: utf-8
from django.test import TestCase
from django.test import Client
from django.core import mail
from django.utils import timezone
from django.conf import settings

from mock import patch
from freezegun import freeze_time

from studygroups.models import generate_all_meetings
from studygroups.models import StudyGroup
from studygroups.models import Profile
from studygroups.models import Team, TeamMembership
from custom_registration.models import create_user


import datetime
import json

class TestLearningCircleApi(TestCase):

    fixtures = ['test_courses.json', 'test_studygroups.json']

    def setUp(self):
        with patch('custom_registration.signals.send_email_confirm_email'):
            user = create_user('faci@example.net', 'b', 't', 'password', False)
            user.save()
            self.facilitator = user


    def test_create_learning_circle(self):
        c = Client()
        c.login(username='faci@example.net', password='password')
        data = {
            "name": "Test learning circle",
            "course": 3,
            "description": "Lets learn something",
            "course_description": "A real great course",
            "venue_name": "75 Harrington",
            "venue_details": "top floor",
            "venue_address": "75 Harrington",
            "city": "Cape Town",
            "country": "South Africa",
            "country_en": "South Africa",
            "region": "Western Cape",
            "latitude": 3.1,
            "longitude": "1.3",
            "place_id": "1",
            "language": "en",
            "start_date": "2018-02-12",
            "weeks": 2,
            "meeting_time": "17:01",
            "duration": 50,
            "timezone": "UTC",
            "image": "/media/image.png",
            "facilitator_concerns": "blah blah",
        }
        url = '/api/learning-circle/'
        self.assertEqual(StudyGroup.objects.all().count(), 4)

        resp = c.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(resp.status_code, 200)

        lc = StudyGroup.objects.all().last()
        self.assertEqual(resp.json(), {
            "status": "created",
            "studygroup_url": "{}://{}/en/studygroup/{}/".format(settings.PROTOCOL, settings.DOMAIN, lc.pk)
        })
        self.assertEqual(StudyGroup.objects.all().count(), 5)
        self.assertEqual(lc.course.id, 3)
        self.assertEqual(lc.name, "Test learning circle")
        self.assertEqual(lc.description, 'Lets learn something')
        self.assertEqual(lc.course_description, 'A real great course')
        self.assertEqual(lc.start_date, datetime.date(2018,2,12))
        self.assertEqual(lc.meeting_time, datetime.time(17,1))
        self.assertEqual(lc.meeting_set.all().count(), 0)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Your “{}” learning circle in {} has been created! What next?'.format(lc.name, lc.city))
        self.assertIn('faci@example.net', mail.outbox[0].to)
        self.assertIn('community@localhost', mail.outbox[0].cc)


    def test_create_learning_circle_without_name_or_course_description(self):
        c = Client()
        c.login(username='faci@example.net', password='password')
        data = {
            "course": 3,
            "description": "Lets learn something",
            "venue_name": "75 Harrington",
            "venue_details": "top floor",
            "venue_address": "75 Harrington",
            "city": "Cape Town",
            "country": "South Africa",
            "country_en": "South Africa",
            "region": "Western Cape",
            "latitude": 3.1,
            "longitude": "1.3",
            "place_id": "1",
            "language": "en",
            "start_date": "2018-02-12",
            "weeks": 2,
            "meeting_time": "17:01",
            "duration": 50,
            "timezone": "UTC",
            "image": "/media/image.png",
            "facilitator_concerns": "blah blah",
        }
        url = '/api/learning-circle/'
        self.assertEqual(StudyGroup.objects.all().count(), 4)

        resp = c.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(resp.status_code, 200)

        lc = StudyGroup.objects.all().last()
        self.assertEqual(resp.json(), {
            "status": "created",
            "studygroup_url": "{}://{}/en/studygroup/{}/".format(settings.PROTOCOL, settings.DOMAIN, lc.pk)
        })
        self.assertEqual(StudyGroup.objects.all().count(), 5)
        self.assertEqual(lc.name, lc.course.title)
        self.assertEqual(lc.course_description, lc.course.caption)


    @freeze_time('2018-01-20')
    def test_create_learning_circle_and_publish(self):
        c = Client()
        c.login(username='faci@example.net', password='password')
        self.facilitator.profile.email_confirmed_at = timezone.now()
        self.facilitator.profile.save()
        data = {
            "name": "Test learning circle",
            "course": 3,
            "description": "Lets learn something",
            "course_description": "A real great course",
            "venue_name": "75 Harrington",
            "venue_details": "top floor",
            "venue_address": "75 Harrington",
            "city": "Cape Town",
            "country": "South Africa",
            "country_en": "South Africa",
            "region": "Western Cape",
            "latitude": 3.1,
            "longitude": "1.3",
            "place_id": "1",
            "language": "en",
            "start_date": "2018-02-12",
            "facilitator_concerns": "blah blah",
            "weeks": 2,
            "meeting_time": "17:01",
            "duration": 50,
            "timezone": "UTC",
            "image": "/media/image.png",
            "draft": False,
        }
        url = '/api/learning-circle/'
        self.assertEqual(StudyGroup.objects.all().count(), 4)
        resp = c.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        lc = StudyGroup.objects.all().last()
        self.assertEqual(resp.json(), {
            "status": "created",
            "studygroup_url": "{}://{}/en/studygroup/{}/".format(settings.PROTOCOL, settings.DOMAIN, lc.pk)
        })
        self.assertEqual(StudyGroup.objects.all().count(), 5)
        self.assertEqual(lc.course.id, 3)
        self.assertEqual(lc.draft, False)
        self.assertEqual(lc.name, "Test learning circle")
        self.assertEqual(lc.description, 'Lets learn something')
        self.assertEqual(lc.course_description, 'A real great course')
        self.assertEqual(lc.start_date, datetime.date(2018,2,12))
        self.assertEqual(lc.meeting_time, datetime.time(17,1))
        self.assertEqual(lc.meeting_set.all().count(), 2)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Your “{}” learning circle in {} has been created! What next?'.format(lc.name, lc.city))
        self.assertIn('faci@example.net', mail.outbox[0].to)
        self.assertIn('community@localhost', mail.outbox[0].cc)


    @freeze_time('2018-01-20')
    def test_create_learning_circle_and_publish_user_unconfirmed(self):
        c = Client()
        c.login(username='faci@example.net', password='password')
        data = {
            "name": "Storytelling with Sharon",
            "course": 3,
            "course_description": "A real great course",
            "description": "Lets learn something",
            "venue_name": "75 Harrington",
            "venue_details": "top floor",
            "venue_address": "75 Harrington",
            "city": "Cape Town",
            "country": "South Africa",
            "country_en": "South Africa",
            "region": "Western Cape",
            "latitude": 3.1,
            "longitude": "1.3",
            "language": "en",
            "start_date": "2018-02-12",
            "weeks": 2,
            "meeting_time": "17:01",
            "duration": 50,
            "timezone": "UTC",
            "image": "/media/image.png",
            "draft": False,
        }
        url = '/api/learning-circle/'
        self.assertEqual(StudyGroup.objects.all().count(), 4)
        resp = c.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        lc = StudyGroup.objects.all().last()
        self.assertEqual(resp.json().get('status'), 'created')
        self.assertEqual(StudyGroup.objects.all().count(), 5)
        self.assertEqual(StudyGroup.objects.last().draft, True)
        self.assertEqual(len(mail.outbox), 1)


    def test_create_learning_circle_welcome(self):
        c = Client()
        c.login(username='faci@example.net', password='password')
        data = {
            "course": 3,
            "description": "Lets learn something",
            "course_description": "A real great course",
            "venue_name": "75 Harrington",
            "venue_details": "top floor",
            "venue_address": "75 Harrington",
            "city": "Cape Town",
            "country": "South Africa",
            "country_en": "South Africa",
            "region": "Western Cape",
            "latitude": 3.1,
            "longitude": "1.3",
            "place_id": "1",
            "language": "en",
            "start_date": "2018-02-12",
            "weeks": 2,
            "meeting_time": "17:01",
            "duration": 50,
            "timezone": "UTC",
            "image": "/media/image.png"
        }
        url = '/api/learning-circle/'
        self.assertEqual(StudyGroup.objects.all().count(), 4)

        # Test without concern only p2pu should be CC-ed
        resp = c.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(resp.status_code, 200)

        lc = StudyGroup.objects.all().last()
        self.assertEqual(resp.json(), {
            "status": "created",
            "studygroup_url": "{}://{}/en/studygroup/{}/".format(settings.PROTOCOL, settings.DOMAIN, lc.pk)
        })
        self.assertEqual(StudyGroup.objects.all().count(), 5)
        self.assertEqual(lc.course.id, 3)
        self.assertEqual(lc.description, 'Lets learn something')
        self.assertEqual(lc.start_date, datetime.date(2018,2,12))
        self.assertEqual(lc.meeting_time, datetime.time(17,1))
        self.assertEqual(lc.meeting_set.all().count(), 0)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Your “{}” learning circle in {} has been created! What next?'.format(lc.name, lc.city))
        self.assertIn('faci@example.net', mail.outbox[0].to)
        self.assertIn('thepeople@p2pu.org', mail.outbox[0].cc)
        self.assertEqual(len(mail.outbox[0].cc), 1)

        # Test with concern - welcome committee should be cc-ed
        mail.outbox = []
        data['facilitator_concerns'] = 'How should I advertise'
        resp = c.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Your “{}” learning circle in {} has been created! What next?'.format(lc.name, lc.city))
        self.assertIn('faci@example.net', mail.outbox[0].to)
        self.assertIn('thepeople@p2pu.org', mail.outbox[0].cc)
        self.assertIn('community@localhost', mail.outbox[0].cc)
        self.assertIn(data['facilitator_concerns'], mail.outbox[0].body)
        self.assertEqual(len(mail.outbox[0].cc), 2)

        # Test as part of team with concern - organizer and welcome should be CC-ed
        team = Team.objects.create(name='awesome team')
        team.save()
        organizer = create_user('org@niz.er', 'organ', 'izer', False)
        TeamMembership.objects.create(team=team, user=organizer, role=TeamMembership.ORGANIZER)
        TeamMembership.objects.create(team=team, user=self.facilitator, role=TeamMembership.MEMBER)

        mail.outbox = []
        resp = c.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Your “{}” learning circle in {} has been created! What next?'.format(lc.name, lc.city))
        self.assertIn('faci@example.net', mail.outbox[0].to)
        self.assertIn('thepeople@p2pu.org', mail.outbox[0].cc)
        self.assertIn('community@localhost', mail.outbox[0].cc)
        self.assertIn('org@niz.er', mail.outbox[0].cc)
        self.assertEqual(len(mail.outbox[0].cc), 3)

        # Test as part of team - team organizer should be cc-ed
        mail.outbox = []
        del data['facilitator_concerns']
        resp = c.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Your “{}” learning circle in {} has been created! What next?'.format(lc.name, lc.city))
        self.assertIn('faci@example.net', mail.outbox[0].to)
        self.assertIn('thepeople@p2pu.org', mail.outbox[0].cc)
        self.assertIn('org@niz.er', mail.outbox[0].cc)
        self.assertEqual(len(mail.outbox[0].cc), 2)

    def test_update_learning_circle(self):
        self.facilitator.profile.email_confirmed_at = timezone.now()
        self.facilitator.profile.save()
        c = Client()
        c.login(username='faci@example.net', password='password')
        data = {
            "course": 3,
            "description": "Lets learn something",
            "course_description": "A real great course",
            "venue_name": "75 Harrington",
            "venue_details": "top floor",
            "venue_address": "75 Harrington",
            "city": "Cape Town",
            "country": "South Africa",
            "country_en": "South Africa",
            "region": "Western Cape",
            "latitude": 3.1,
            "longitude": "1.3",
            "place_id": "4",
            "language": "en",
            "start_date": "2018-12-12",
            "weeks": 2,
            "meeting_time": "17:01",
            "duration": 50,
            "timezone": "UTC",
            "image": "/media/image.png",
            "draft": False
        }
        url = '/api/learning-circle/'
        self.assertEqual(StudyGroup.objects.all().count(), 4)

        resp = c.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        lc = StudyGroup.objects.all().last()
        self.assertEqual(resp.json(), {
            "status": "created",
            "studygroup_url": "{}://{}/en/studygroup/{}/".format(settings.PROTOCOL, settings.DOMAIN, lc.pk)
        })
        self.assertEqual(StudyGroup.objects.all().count(), 5)

        # Update learning circle
        lc = StudyGroup.objects.all().last()
        self.assertFalse(lc.draft)
        url = '/api/learning-circle/{}/'.format(lc.pk)
        data['course'] = 1
        data["description"] = "Lets learn something else"

        # date shouldn't matter, but lets make it after the lc started
        with freeze_time('2019-03-01'):
            resp = c.post(url, data=json.dumps(data), content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json()['status'], 'updated')

        lc = StudyGroup.objects.all().last()
        self.assertEqual(StudyGroup.objects.all().count(), 5)
        self.assertEqual(lc.course.id, 1)
        self.assertEqual(lc.description, "Lets learn something else")


    def test_update_learning_circle_date(self):
        c = Client()
        c.login(username='faci@example.net', password='password')
        self.facilitator.profile.email_confirmed_at = timezone.now()
        self.facilitator.profile.save()
        data = {
            "course": 3,
            "description": "Lets learn something",
            "course_description": "A real great course",
            "venue_name": "75 Harrington",
            "venue_details": "top floor",
            "venue_address": "75 Harrington",
            "city": "Cape Town",
            "country": "South Africa",
            "country_en": "South Africa",
            "region": "Western Cape",
            "latitude": 3.1,
            "longitude": "1.3",
            "place_id": "4",
            "language": "en",
            "start_date": "2018-12-15",
            "weeks": 2,
            "meeting_time": "17:01",
            "duration": 50,
            "timezone": "UTC",
            "image": "/media/image.png",
            "draft": False
        }
        url = '/api/learning-circle/'
        self.assertEqual(StudyGroup.objects.all().count(), 4)
        resp = c.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(resp.status_code, 200)

        lc = StudyGroup.objects.all().last()
        self.assertEqual(resp.json(), {
            "status": "created",
            "studygroup_url": "{}://{}/en/studygroup/{}/".format(settings.PROTOCOL, settings.DOMAIN, lc.pk)
        })
        self.assertEqual(StudyGroup.objects.all().count(), 5)
        self.assertEqual(lc.meeting_set.active().count(), 2)

        # update less than 2 days before start
        with freeze_time("2018-12-14"):
            data['start_date'] = '2018-12-20'
            data['weeks'] = 6
            url = '/api/learning-circle/{}/'.format(lc.pk)
            resp = c.post(url, data=json.dumps(data), content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json(), {
                "status": "error",
                "errors": {"start_date": "cannot update date"},
            })
            lc = StudyGroup.objects.all().last()
            self.assertEqual(StudyGroup.objects.all().count(), 5)
            self.assertEqual(lc.start_date, datetime.date(2018, 12, 15))
            self.assertEqual(lc.meeting_set.active().count(), 2)

        # update more than 2 days before start
        with freeze_time("2018-12-12"):
            data['start_date'] = '2018-12-19'
            data['weeks'] = 6
            url = '/api/learning-circle/{}/'.format(lc.pk)
            resp = c.post(url, data=json.dumps(data), content_type='application/json')
            self.assertEqual(resp.json(), {
                "status": "updated",
            "studygroup_url": "{}://{}/en/studygroup/{}/".format(settings.PROTOCOL, settings.DOMAIN, lc.pk)
            })

            lc = StudyGroup.objects.all().last()
            self.assertEqual(StudyGroup.objects.all().count(), 5)
            self.assertEqual(lc.start_date, datetime.date(2018, 12, 19))
            self.assertEqual(lc.meeting_set.active().count(), 6)


    def test_update_draft_learning_circle_date(self):
        c = Client()
        c.login(username='faci@example.net', password='password')
        self.facilitator.profile.email_confirmed_at = timezone.now()
        self.facilitator.profile.save()
        data = {
            "course": 3,
            "description": "Lets learn something",
            "course_description": "A real great course",
            "venue_name": "75 Harrington",
            "venue_details": "top floor",
            "venue_address": "75 Harrington",
            "city": "Cape Town",
            "country": "South Africa",
            "country_en": "South Africa",
            "region": "Western Cape",
            "latitude": 3.1,
            "longitude": "1.3",
            "place_id": "4",
            "language": "en",
            "start_date": "2018-12-15",
            "weeks": 2,
            "meeting_time": "17:01",
            "duration": 50,
            "timezone": "UTC",
            "image": "/media/image.png",
            "draft": True
        }
        url = '/api/learning-circle/'
        self.assertEqual(StudyGroup.objects.all().count(), 4)
        with freeze_time('2018-12-01'):
            resp = c.post(url, data=json.dumps(data), content_type='application/json')
            self.assertEqual(resp.status_code, 200)

        lc = StudyGroup.objects.all().last()
        self.assertEqual(resp.json(), {
            "status": "created",
            "studygroup_url": "{}://{}/en/studygroup/{}/".format(settings.PROTOCOL, settings.DOMAIN, lc.pk)
        })
        self.assertEqual(StudyGroup.objects.all().count(), 5)
        self.assertEqual(lc.meeting_set.active().count(), 0)

        # update less than 2 days before
        with freeze_time("2018-12-14"):
            data['start_date'] = '2018-12-20'
            data['weeks'] = 6
            url = '/api/learning-circle/{}/'.format(lc.pk)
            resp = c.post(url, data=json.dumps(data), content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json(), {
                "status": "updated",
            "studygroup_url": "{}://{}/en/studygroup/{}/".format(settings.PROTOCOL, settings.DOMAIN, lc.pk)
            })
            lc = StudyGroup.objects.all().last()
            self.assertEqual(StudyGroup.objects.all().count(), 5)
            self.assertEqual(lc.start_date, datetime.date(2018, 12, 20))
            self.assertEqual(lc.meeting_set.active().count(), 0)

        # update more than 2 days before
        with freeze_time("2018-12-12"):
            data['start_date'] = '2018-12-19'
            data['weeks'] = 6
            url = '/api/learning-circle/{}/'.format(lc.pk)
            resp = c.post(url, data=json.dumps(data), content_type='application/json')
            self.assertEqual(resp.json(), {
                "status": "updated",
            "studygroup_url": "{}://{}/en/studygroup/{}/".format(settings.PROTOCOL, settings.DOMAIN, lc.pk)
            })
            lc = StudyGroup.objects.all().last()
            self.assertEqual(StudyGroup.objects.all().count(), 5)
            self.assertEqual(lc.start_date, datetime.date(2018, 12, 19))
            self.assertEqual(lc.meeting_set.active().count(), 0)



    @freeze_time('2018-01-20')
    def test_publish_learning_circle(self):
        self.facilitator.profile.email_confirmed_at = timezone.now()
        self.facilitator.profile.save()
        c = Client()
        c.login(username='faci@example.net', password='password')
        data = {
            "course": 3,
            "description": "Lets learn something",
            "course_description": "A real great course",
            "venue_name": "75 Harrington",
            "venue_details": "top floor",
            "venue_address": "75 Harrington",
            "city": "Cape Town",
            "country": "South Africa",
            "country_en": "South Africa",
            "region": "Western Cape",
            "latitude": 3.1,
            "longitude": "1.3",
            "place_id": "4",
            "language": "en",
            "start_date": "2018-02-12",
            "weeks": 2,
            "meeting_time": "17:01",
            "duration": 50,
            "timezone": "UTC",
            "image": "/media/image.png"
        }
        url = '/api/learning-circle/'
        self.assertEqual(StudyGroup.objects.all().count(), 4)
        resp = c.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        lc = StudyGroup.objects.all().last()
        self.assertEqual(resp.json(), {
            "status": "created",
            "studygroup_url": "{}://{}/en/studygroup/{}/".format(settings.PROTOCOL, settings.DOMAIN, lc.pk)
        })
        self.assertEqual(StudyGroup.objects.all().count(), 5)
        self.assertEqual(lc.meeting_set.all().count(), 0)
        data['draft'] = False
        # Update learning circle
        url = '/api/learning-circle/{}/'.format(lc.pk)
        resp = c.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        lc = StudyGroup.objects.all().last()
        self.assertEqual(resp.json()['status'], 'updated')
        self.assertEqual(StudyGroup.objects.all().count(), 5)
        self.assertEqual(lc.meeting_set.all().count(), 2)


    def test_get_learning_circles(self):
        c = Client()
        resp = c.get('/api/learningcircles/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["count"], 4)


    def test_get_learning_circles_unicode(self):
        self.facilitator.profile.email_confirmed_at = timezone.now()
        self.facilitator.profile.save()
        c = Client()
        c.login(username='faci@example.net', password='password')
        data = {
            "course": 3,
            "description": "Lets learn something",
            "course_description": "A real great course",
            "venue_name": "الصحة النفسية للطفل",
            "venue_details": "top floor",
            "venue_address": "75 Harrington",
            "city": "Cape Town",
            "country": "South Africa",
            "country_en": "South Africa",
            "region": "Western Cape",
            "latitude": 3.1,
            "longitude": "1.3",
            "place_id": "4",
            "language": "en",
            "start_date": "2018-02-12",
            "weeks": 2,
            "meeting_time": "17:01",
            "duration": 50,
            "timezone": "UTC",
            "image": "/media/image.png",
            "draft": False,
        }
        url = '/api/learning-circle/'
        self.assertEqual(StudyGroup.objects.all().count(), 4)
        with freeze_time('2018-01-20'):
            resp = c.post(url, data=json.dumps(data), content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            lc = StudyGroup.objects.all().last()
            self.assertEqual(resp.json(), {
                "status": "created",
                "studygroup_url": "{}://{}/en/studygroup/{}/".format(settings.PROTOCOL, settings.DOMAIN, lc.pk)
            })
            self.assertEqual(StudyGroup.objects.all().count(), 5)

        c = Client()
        resp = c.get('/api/learningcircles/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["count"], 5)


    def test_get_learning_circles_invalid_venue_name(self):
        self.facilitator.profile.email_confirmed_at = timezone.now()
        self.facilitator.profile.save()
        c = Client()
        c.login(username='faci@example.net', password='password')
        data = {
            "course": 3,
            "description": "Lets learn something",
            "course_description": "A real great course",
            "venue_name": "/@@",
            "venue_details": "top floor",
            "venue_address": "75 Harrington",
            "city": "Cape Town",
            "country": "South Africa",
            "country_en": "South Africa",
            "region": "Western Cape",
            "latitude": 3.1,
            "longitude": "1.3",
            "place_id": "4",
            "language": "en",
            "start_date": "2018-02-12",
            "weeks": 2,
            "meeting_time": "17:01",
            "duration": 50,
            "timezone": "UTC",
            "image": "/media/image.png",
            "draft": False,
        }
        url = '/api/learning-circle/'
        self.assertEqual(StudyGroup.objects.all().count(), 4)
        with freeze_time('2018-01-20'):
            resp = c.post(url, data=json.dumps(data), content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json(), {
                "status": "error",
                "errors": {"venue_name": [
                    'Venue name should include at least one alpha-numeric character.'
                ]},
            })
            self.assertEqual(StudyGroup.objects.all().count(), 4)


    def test_get_learning_circles_exclude_drafts(self):
        c = Client()
        sg = StudyGroup.objects.get(pk=1)
        sg.draft = True
        sg.save()
        resp = c.get('/api/learningcircles/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["count"], 3)


    def test_get_learning_circles_by_weekday(self):
        sg = StudyGroup.objects.get(pk=1)
        sg.start_date = datetime.date(2018,1,26)
        sg.save()
        sg = StudyGroup.objects.get(pk=2)
        sg.start_date = datetime.date(2018,1,27)
        sg.save()
        c = Client()
        # Friday and Saturday
        resp = c.get('/api/learningcircles/?weekdays=4,5')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["count"], 2)


    def test_get_learning_circles_full_text_search(self):
        c = Client()

        # partial word match

        resp = c.get('/api/learningcircles/', {'q': 'aca'})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["count"], 2)
        self.assertEqual(data["items"][0]["course"]["title"], "Academic Writing")
        self.assertEqual(data["items"][1]["course"]["provider"], "Khan Academy")

        resp = c.get('/api/learningcircles/', {'q': 'acad'})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["count"], 2)
        self.assertEqual(data["items"][0]["course"]["title"], "Academic Writing")
        self.assertEqual(data["items"][1]["course"]["provider"], "Khan Academy")

        resp = c.get('/api/learningcircles/', {'q': 'acade'})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["count"], 2)
        self.assertEqual(data["items"][0]["course"]["title"], "Academic Writing")
        self.assertEqual(data["items"][1]["course"]["provider"], "Khan Academy")

        resp = c.get('/api/learningcircles/', {'q': 'academ'})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["count"], 2)
        self.assertEqual(data["items"][0]["course"]["title"], "Academic Writing")
        self.assertEqual(data["items"][1]["course"]["provider"], "Khan Academy")

        resp = c.get('/api/learningcircles/', {'q': 'writ'})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["items"][0]["course"]["title"], "Academic Writing")

        resp = c.get('/api/learningcircles/', {'q': 'writing'})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["items"][0]["course"]["title"], "Academic Writing")


        # full word match

        resp = c.get('/api/learningcircles/', {'q': 'academy'})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["items"][0]["course"]["provider"], "Khan Academy")

        resp = c.get('/api/learningcircles/', {'q': 'academic'})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["items"][0]["course"]["title"], "Academic Writing")


    @freeze_time("2019-05-31")
    def test_get_learning_circles_by_scope(self):
        sg = StudyGroup.objects.get(pk=1)
        sg.start_date = datetime.date(2019,6,1)
        sg.end_date = sg.start_date + datetime.timedelta(weeks=2)
        sg.save()
        sg.refresh_from_db()
        generate_all_meetings(sg)

        sg = StudyGroup.objects.get(pk=2)
        sg.start_date = datetime.date(2019,5,30)
        sg.end_date = sg.start_date + datetime.timedelta(weeks=2)
        sg.save()
        sg.refresh_from_db()
        generate_all_meetings(sg)

        sg = StudyGroup.objects.get(pk=3)
        sg.start_date = datetime.date(2019,5,1)
        sg.end_date = sg.start_date + datetime.timedelta(weeks=2)
        sg.save()
        sg.refresh_from_db()
        generate_all_meetings(sg)

        sg = StudyGroup.objects.get(pk=4)
        sg.start_date = datetime.date(2019,5,30)
        sg.end_date = sg.start_date + datetime.timedelta(weeks=2)
        sg.draft = True
        sg.save()

        c = Client()

        # active scope
        resp = c.get('/api/learningcircles/?scope=active&draft=true')
        data = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data["count"], 3)
        self.assertEqual(data["items"][0]["id"], 1)
        self.assertEqual(data["items"][1]["id"], 2)
        self.assertEqual(data["items"][2]["id"], 4)
        self.assertEqual(data["items"][2]["draft"], True)

        # completed scope
        resp = c.get('/api/learningcircles/?scope=completed')
        data = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["count"], 1)
        self.assertEqual(data["items"][0]["id"], 3)


    @freeze_time("2019-05-31")
    def test_get_learning_circles_next_meeting(self):
        sg = StudyGroup.objects.get(pk=1)
        sg.start_date = datetime.date(2019,5,30)
        sg.end_date = sg.start_date + datetime.timedelta(weeks=2)
        sg.save()
        sg.refresh_from_db()
        generate_all_meetings(sg)

        c = Client()

        resp = c.get('/api/learningcircles/?scope=active')
        data = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["count"], 1)
        self.assertEqual(data["items"][0]["next_meeting_date"], "2019-06-06")


    @freeze_time("2019-05-31")
    def test_get_learning_circles_last_meeting(self):
        sg = StudyGroup.objects.get(pk=1)
        sg.start_date = datetime.date(2019,5,1)
        sg.end_date = sg.start_date + datetime.timedelta(weeks=2)
        sg.save()
        sg.refresh_from_db()
        generate_all_meetings(sg)

        c = Client()

        resp = c.get('/api/learningcircles/?scope=completed')
        data = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["count"], 1)
        self.assertEqual(data["items"][0]["last_meeting_date"], "2019-05-15")
