from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from api.models import Image
from django.shortcuts import HttpResponse
import uuid
import json


class ImageTool:
    @staticmethod
    def get_new_random_file_name(file_name):
        find_type = False
        for c in file_name:
            if c == '.':
                find_type = True
        if find_type:
            type = file_name.split('.')[-1]
            return str(uuid.uuid1()) + '.' + type
        else:
            return str(uuid.uuid1())


@csrf_exempt
def image_upload(request):
    if request.method != "POST":
        return HttpResponse()
    source = request.FILES.get('file')
    if source != None:
        source.name = ImageTool.get_new_random_file_name(source.name)
        image = Image(
            img=source
        )
        image.save()
        return HttpResponse(json.dumps({
            'success': True,
            'path': image.img.url
        }))
    else:
        return HttpResponse(json.dumps({
            'success': False,
        }))
