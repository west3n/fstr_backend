from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
import json
from .models import User, Area, MountainPass
from .serializers import UserSerializer, AreaSerializer, MountainPassSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer


class MountainPassViewSet(viewsets.ModelViewSet):
    queryset = MountainPass.objects.all()
    serializer_class = MountainPassSerializer


@csrf_exempt
def submitData(request):
    if request.method == 'POST':
        json_params = json.loads(request.body)

        mountain_pass = MountainPass.objects.create(
            title=json_params['title'],
            alt_title=json_params['alt_title'],
            longitude=json_params['longitude'],
            latitude=json_params['latitude'],
            height=json_params['height'],
            images=json_params['images'],
            user=User.objects.create(
                first_name=json_params['first_name'],
                last_name=json_params['last_name'],
                email=json_params['email'],
                phoneNumber=json_params['phoneNumber']

            )

        )
        return HttpResponse(json.dumps({
            "title": mountain_pass.title,
            "alt_title": mountain_pass.alt_title,
            "longitude": mountain_pass.longitude,
            "latitude": mountain_pass.latitude,
            "height": mountain_pass.height,
            "images": mountain_pass.images,
            "user": mountain_pass.user,
        }))


def submitData_get_patch(request, mountain_pass_id):
    mountain_pass = MountainPass.objects.get(id=mountain_pass_id)
    if request.method == 'GET':
        return HttpResponse(json.dumps(
            {
                "title": mountain_pass.title,
                "alt_title": mountain_pass.alt_title,
                "longitude": mountain_pass.longitude,
                "latitude": mountain_pass.latitude,
                "height": mountain_pass.height,
                "images": mountain_pass.images,
                "user": mountain_pass.user,
            }))
    json_params = json.loads(request.body)
    if request.method == 'PATCH':
        mountain_pass.title = json_params.get('title', mountain_pass.title)
        mountain_pass.alt_title = json_params.get('alt_title', mountain_pass.alt_title)
        mountain_pass.longitude = json_params.get('longitude', mountain_pass.longitude)
        mountain_pass.latitude = json_params.get('latitude', mountain_pass.latitude)
        mountain_pass.height = json_params.get('height', mountain_pass.height)
        mountain_pass.images = json_params.get('images', mountain_pass.images)
        mountain_pass.save()
        return HttpResponse(json.dumps({
            "title": mountain_pass.title,
            "alt_title": mountain_pass.alt_title,
            "longitude": mountain_pass.longitude,
            "latitude": mountain_pass.latitude,
            "height": mountain_pass.height,
            "images": mountain_pass.images,
        }))
