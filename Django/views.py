from django.contrib.auth.models import Group
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import viewsets
from Django.serializers import ZerotierDeviceSerializer, DeviceDetailsSerializer, ZerotierRequestSerializer, \
    GroupSerializer, UserSerializer, EmptyPayloadResponseSerializer
from Django.models import DeviceDetails, ZerotierDevices, ZerotierRequestAccess, User


class HttpResponse:
    def error404(self):
        return


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


ZT_DEVICE = 'ztdevice'
ZT_DEVICE_REQUEST = 'ztdevicerequest'
ZT_DEVICE_DETAIL = 'ztdevicedetails'


@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
@extend_schema(request=EmptyPayloadResponseSerializer, responses=EmptyPayloadResponseSerializer)
def zt_devices_cr(request, table_name):
    """
        List all devices records
    """
    if request.method == 'GET':
        # TODO: not tweaked to only check 2nd URI, checking whole URI is not ideal
        if ZT_DEVICE == table_name:
            ztdevices = ZerotierDevices.objects.all()
            serializer = ZerotierDeviceSerializer(ztdevices, many=True)
            return JsonResponse(serializer.data, safe=False)
        elif ZT_DEVICE_REQUEST == table_name:
            ztdevices_request = ZerotierRequestAccess.objects.all()
            serializer = ZerotierRequestSerializer(ztdevices_request, many=True)
            return JsonResponse(serializer.data, safe=False)
        elif ZT_DEVICE_DETAIL == table_name:
            ztdevices_details = DeviceDetails.objects.all()
            serializer = DeviceDetailsSerializer(ztdevices_details, many=True)
            return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        """
            List create new records
        """
        # TODO: check how polymorph work in Python to tweak these 2 statements
        data = request.data
        if ZT_DEVICE == table_name:
            serializer = ZerotierDeviceSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_200_OK)
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST)
        elif ZT_DEVICE_REQUEST == table_name:
            serializer = ZerotierRequestSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_200_OK)
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif ZT_DEVICE_DETAIL == table_name:
            serializer = DeviceDetailsSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_200_OK)
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'GET'])
@permission_classes((permissions.AllowAny,))
@extend_schema(request=EmptyPayloadResponseSerializer,
               responses={201: (ZerotierDeviceSerializer, ZerotierRequestSerializer, DeviceDetailsSerializer)})
def zt_devices_ud(request, table_name, pk=0):
    """
       Get devices by id
    """
    if request.method == 'GET':
        if ZT_DEVICE == table_name:
            try:
                ztdevices = ZerotierDevices.objects.get(pk=pk)
                data = ZerotierDeviceSerializer(ztdevices)
                if data.data is not None:
                    return JsonResponse(data.data, status=status.HTTP_200_OK)
            except ZerotierDevices.DoesNotExist:
                return JsonResponse(status=status.HTTP_404_NOT_FOUND)
        elif ZT_DEVICE_REQUEST == table_name:
            try:
                ztdevices_request = ZerotierRequestAccess.objects.get(pk=pk)
                data = ZerotierRequestSerializer(ztdevices_request)
                if data.data is not None:
                    return JsonResponse(data.data, status=status.HTTP_200_OK)
            except ZerotierRequestAccess.DoesNotExist:
                return JsonResponse(status=status.HTTP_404_NOT_FOUND)
        elif ZT_DEVICE_DETAIL == table_name:
            try:
                ztdevices_details = DeviceDetails.objects.get(pk=pk)
                data = DeviceDetailsSerializer(ztdevices_details)
                if data.data is not None:
                    return JsonResponse(data.data, status=status.HTTP_200_OK)
            except DeviceDetails.DoesNotExist:
                return JsonResponse(status=status.HTTP_404_NOT_FOUND)

    """
        Update Device Records
    """
    if request.method == 'PUT':
        if ZT_DEVICE == table_name:
            try:
                ztdevices = ZerotierDevices.objects.get(pk=pk)
            except ZerotierDevices.DoesNotExist:
                return JsonResponse(ZerotierDevices.DoesNotExist, status=status.HTTP_404_NOT_FOUND)
            json = request.data
            serializer = ZerotierDeviceSerializer(ztdevices, data=json)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        elif ZT_DEVICE_REQUEST == table_name:
            try:
                ztdevices = ZerotierRequestAccess.objects.get(pk=pk)
            except ZerotierRequestAccess.DoesNotExist:
                return JsonResponse(ZerotierRequestAccess.DoesNotExist, status=status.HTTP_404_NOT_FOUND)
            json = request.data
            serializer = ZerotierRequestSerializer(ztdevices, data=json)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        elif ZT_DEVICE_DETAIL == table_name:
            try:
                ztdevices = DeviceDetails.objects.get(pk=pk)
            except DeviceDetails.DoesNotExist:
                return JsonResponse(DeviceDetails.DoesNotExist, status=status.HTTP_404_NOT_FOUND)
            json = request.data
            serializer = DeviceDetailsSerializer(ztdevices, data=json)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
@extend_schema(request=ZerotierRequestAccess,
               responses={201: ZerotierDeviceSerializer})
def zt_approve(request, pk=0):
    """Approve the request device"""
    try:
        ztdevices = ZerotierRequestAccess.objects.get(pk=pk)
    except ZerotierRequestAccess.DoesNotExist:
        return JsonResponse(ZerotierRequestAccess.DoesNotExist, status=status.HTTP_404_NOT_FOUND)
    data = ZerotierRequestSerializer(ztdevices, many=False).data
    serializer = ZerotierDeviceSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        ztdevices.delete()
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    return JsonResponse(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
