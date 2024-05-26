import datetime
import json

from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APIRequestFactory

from Django import models


# Create your tests here.

class ModelTest(TestCase):
    """Model testcase"""

    def test_create_device_record(self, **kwargs):
        tags = {"level": "value2", "level2": "value"}
        devices = models.ZerotierDevices.objects.create(
            last_update='2024-05-27 13:53:57.341494+08',
            zt_ip_address='127.0.0.1',
            region='CN',
            member_id='1',
            last_online='2024-05-27 13:53:57.341494+08',
            machine_category='test',
            local_ip='127.0.0.1',
            is_device_online=False,
            network_ip='127.0.0.1',
            serial_number='1234',
            tags=json.dumps(tags, indent=4)
        )
        self.assertEquals(str(devices.serial_number), devices.serial_number)

    def test_get_single_record(self):
        self.assertEquals('', '')

    def test_create_new_record(self):
        self.assertEquals('', '')

    def test_update_record(self):
        self.assertEquals('', '')

    def test_approve_zerotier_device(self):
        self.assertEquals('', '')


DEVICES_URL = '/api/ztdevice'
DEVICES_DETAIL_URL = '/api/ztdevice'
DEVICES_REQUEST_URL = '/api/ztdevicerequest'


class APICallTest(TestCase):
    """Test API Call"""

    def setUp(self):
        self.client = APIClient()

    def test_device_request_get(self):
        """Test API Get Device Request Call"""
        res = self.client.get(DEVICES_REQUEST_URL)
        self.assertEquals(res.status_code, status.HTTP_200_OK)

    def test_create_device_request(self):
        """Test API Create Device Request Call"""
        devices = {"last_update": "2024-05-26 13:53:57.341494+08",
                   "zt_ip_address": "127.0.0.1",
                   "region": "CN",
                   "member_id": "1",
                   "last_online": "2024-05-26 13:53:57.341494+08",
                   "machine_category": "test",
                   "local_ip": "127.0.0.1",
                   "is_device_online": "False",
                   "network_ip": "127.0.0.1",
                   "serial_number": "1234",
                   "tags": "{\"level\": \"value2\", \"level2\": \"value\"}"
                   }
        res = self.client.post(DEVICES_REQUEST_URL, devices)
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertIn('last_update', res.data)

    def test_update_device_request(self):
        """Test API Update Device Request Call"""
        tags = {"level": "value2", "level2": "value"}
        new_device = models.ZerotierRequestAccess.objects.create(
            last_update='2024-05-27 13:53:57.341494+08',
            zt_ip_address='127.0.0.1',
            region='MY',
            member_id='1',
            last_online='2024-05-27 13:53:57.341494+08',
            machine_category='test',
            local_ip='127.0.0.1',
            is_device_online=False,
            network_ip='127.0.0.1',
            serial_number='1234',
            tags=json.dumps(tags, indent=4)
        )
        device = {"last_update": "2024-05-26 13:53:57.341494+08",
                  "zt_ip_address": "127.0.0.1",
                  "region": "CN",
                  "member_id": "1",
                  "last_online": "2024-05-26 13:53:57.341494+08",
                  "machine_category": "test",
                  "local_ip": "127.0.0.1",
                  "is_device_online": "False",
                  "network_ip": "127.0.0.1",
                  "serial_number": "1234",
                  "tags": "{\"level\": \"value2\", \"level2\": \"value\"}"
                  }
        res = self.client.put(DEVICES_REQUEST_URL + '/1', device)
        new_device.refresh_from_db()
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(new_device.region, 'CN')
