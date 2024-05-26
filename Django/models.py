from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin, AbstractUser
)
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.functions import datetime


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_field):
        user = self.model(email=email, **extra_field)
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    object = UserManager()


class DeviceDetails(models.Model):
    last_update = models.DateTimeField(default=datetime.Now)
    serial_number = models.CharField(max_length=100, default='')
    machine_category = models.CharField(max_length=100, default='')
    system_image = models.CharField(max_length=255, default='')
    eth0_mac_address = models.CharField(max_length=17, default='')
    eth1_mac_address = models.CharField(max_length=17, default='')

    def __str__(self):
        return self.serial_number

    class Meta:
        db_table = 'device_details'


class AbstractZerotier(models.Model):
    last_update = models.DateTimeField(blank=True)  # TODO: Replace with timedate Now; having error previously
    zt_ip_address = models.CharField(max_length=45, default='')
    region = models.CharField(max_length=100, default='')
    member_id = models.CharField(max_length=100, default='')
    last_online = models.DateTimeField(blank=True)
    machine_category = models.CharField(max_length=100, default='')
    local_ip = models.CharField(max_length=45, default='')
    network_ip = models.CharField(max_length=100, default='')
    serial_number = models.CharField(max_length=100, default='')
    is_device_online = models.BooleanField()
    tags = models.JSONField(dict)

    def __str__(self):
        return self.zt_ip_address

    class Meta:
        abstract = True


class ZerotierDevices(AbstractZerotier):
    class Meta:
        db_table = 'zerotier_devices'


class ZerotierRequestAccess(AbstractZerotier):
    class Meta:
        db_table = 'zerotier_request_access'
