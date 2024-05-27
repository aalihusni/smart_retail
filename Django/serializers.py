from django.contrib.auth.models import Group, User
from rest_framework import serializers
from Django.models import DeviceDetails, ZerotierDevices, ZerotierRequestAccess


class EmptyPayloadResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class DeviceDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceDetails
        fields = ['last_update', 'serial_number', 'machine_category', 'system_image', 'eth0_mac_address',
                  'eth1_mac_address']

    def create(self, **validated_data):
        """Create Device Detail"""


class ZerotierDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZerotierDevices
        fields = ['last_update', 'zt_ip_address', 'region', 'member_id', 'last_online', 'machine_category', 'local_ip',
                  'network_ip', 'serial_number', 'is_device_online', 'tags']

    def create(self, validated_data):
        """Create ZT Device"""
        devices = ZerotierDevices.objects.create(**validated_data)
        return devices

    def update(self, instance, validated_data):
        """Update ZT Device"""
        instance.last_update = validated_data.get('last_update', instance.last_update)
        instance.zt_ip_address = validated_data.get('zt_ip_address', instance.zt_ip_address)
        instance.region = validated_data.get('region', instance.region)
        instance.member_id = validated_data.get('member_id', instance.member_id)
        instance.last_online = validated_data.get('last_online', instance.last_online)
        instance.machine_category = validated_data.get('machine_category', instance.machine_category)
        instance.local_ip = validated_data.get('local_ip', instance.local_ip)
        instance.network_ip = validated_data.get('network_ip', instance.network_ip)
        instance.serial_number = validated_data.get('serial_number', instance.serial_number)
        instance.is_device_online = validated_data.get('is_device_online', instance.is_device_online)
        instance.tags = validated_data.get('tags', instance.tags)
        instance.save()
        return instance


class ZerotierRequestSerializer(serializers.ModelSerializer):
    class Meta:
        # TODO remove duplicated code
        model = ZerotierRequestAccess
        fields = ['last_update', 'zt_ip_address', 'region', 'member_id', 'last_online', 'machine_category', 'local_ip',
                  'network_ip', 'serial_number', 'is_device_online', 'tags']

    def create(self, validated_data):
        """Create ZT Device Request"""
        devices = ZerotierRequestAccess.objects.create(**validated_data)
        return devices

    def update(self, instance, validated_data):
        """Update ZT Device Request"""
        instance.last_update = validated_data.get('last_update', instance.last_update)
        instance.zt_ip_address = validated_data.get('zt_ip_address', instance.zt_ip_address)
        instance.region = validated_data.get('region', instance.region)
        instance.member_id = validated_data.get('member_id', instance.member_id)
        instance.last_online = validated_data.get('last_online', instance.last_online)
        instance.machine_category = validated_data.get('machine_category', instance.machine_category)
        instance.local_ip = validated_data.get('local_ip', instance.local_ip)
        instance.network_ip = validated_data.get('network_ip', instance.network_ip)
        instance.serial_number = validated_data.get('serial_number', instance.serial_number)
        instance.is_device_online = validated_data.get('is_device_online', instance.is_device_online)
        instance.tags = validated_data.get('tags', instance.tags)
        instance.save()
        return instance
