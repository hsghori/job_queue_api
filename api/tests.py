import json
from unittest import mock
from datetime import datetime
from django.utils import timezone
from django.test import TestCase
from api.models import Job


class TestApiList(TestCase):

    def setUp(self):
        super().setUp()
        statuses = ['Q', 'C', 'P', 'F']
        for idx, status in enumerate(statuses, start=1):
            Job.objects.create(
                url=f'url_{idx}',
                result=f'res_{idx}',
                status=status,
                time_created=datetime(2018, idx, 1, tzinfo=timezone.utc),
                time_updated=datetime(2018, idx, 2, tzinfo=timezone.utc),
            )

    def test_list_no_filters(self):
        url = '/api/job/'
        response = self.client.get(url, content_type='application/json')
        assert response.status_code == 200
        data = response.json()
        assert len(data) == len(Job.objects.all())

    def test_list_url_filters(self):
        url = '/api/job/?url=url_1'
        response = self.client.get(url, content_type='application/json')
        assert response.status_code == 200
        data = response.json()
        assert all([d['url'] == 'url_1' for d in data])

    def test_list_status_filter(self):
        url = '/api/job/?status=C'
        response = self.client.get(url, content_type='application/json')
        assert response.status_code == 200
        data = response.json()
        assert all([d['status'] == 'C' for d in data])

    def test_list_latest_flag(self):
        url = '/api/job/?latest=True'
        response = self.client.get(url, content_type='application/json')
        assert response.status_code == 200
        data = response.json()
        assert data[0]['url'] == 'url_4'


class TestApiCreate(TestCase):

    @mock.patch('api.views.process_job')
    def test_generic_create(self, mock_process_job):
        url = '/api/job/'
        post_data = {
            'url': 'https://www.google.com'
        }
        response = self.client.post(url, data=json.dumps(post_data), content_type='application/json')
        assert response.status_code == 200
        data = response.json()
        assert data['url'] == post_data['url']
        assert data['status'] == 'Q'

    @mock.patch('api.views.datetime')
    @mock.patch('api.views.process_job')
    def test_create_with_job_in_pipeline(self, mock_process_job, mock_datetime):
        url = '/api/job/'
        Job.objects.create(
            url=f'https://www.google.com',
            status='Q',
            time_created=datetime(2018, 1, 1, 2, 3, 4, tzinfo=timezone.utc),
        )
        post_data = {
            'url': 'https://www.google.com'
        }
        mock_datetime.now.return_value = datetime(2018, 1, 1, 2, 4, 5, tzinfo=timezone.utc)
        response = self.client.post(url, data=json.dumps(post_data), content_type='application/json')
        assert response.status_code == 400
        assert response.json() == ["Request to https://www.google.com has been submitted within the last hour"]

    @mock.patch('api.views.datetime')
    @mock.patch('api.views.process_job')
    def test_create_with_completed_job(self, mock_process_job, mock_datetime):
        url = '/api/job/'
        Job.objects.create(
            url=f'https://www.google.com',
            status='Q',
            time_created=datetime(2018, 1, 1, 2, 3, 4, tzinfo=timezone.utc),
        )
        post_data = {
            'url': 'https://www.google.com'
        }
        mock_datetime.now.return_value = datetime(2018, 1, 1, 4, 4, 5, tzinfo=timezone.utc)
        response = self.client.post(url, data=json.dumps(post_data), content_type='application/json')
        assert response.status_code == 200
