from rest_framework import viewsets
from django.http import HttpResponse
from django.shortcuts import render
from .producer import publish
from utils import ThreadSafeDict
import uuid
import base64
import time

proc_dict = ThreadSafeDict()

class ProductViewSet(viewsets.ViewSet):
    def home(self, request):
        template = 'es/home.html'
        return render(request, template)

    def image(self, request):
        image_file = request.FILES.get('image')
        if image_file:
            chunks = []
            for chunk in image_file.chunks():
                chunks.append(chunk)
            byte_string = b''.join(chunks)
            request_uuid = str(uuid.uuid4())
            publish({"uuid": request_uuid, "image": byte_string})
            
            proc_dict.update_dict(request_uuid, (False, None))
            while not proc_dict.get_dict_value(request_uuid)[0]:
                time.sleep(0.5)
                print("wait")
            
            encoded_image = proc_dict.get_dict_value(request_uuid)[1]
            proc_dict.delete_from_dict(request_uuid)
            template = 'es/image.html'
            return render(request, template, {"encoded_image": encoded_image})

    def internal(self, request):
        print("here")
        image = request.POST.get("image").encode('latin-1')
        base64_image = base64.b64encode(image).decode('utf-8')
        uuid = request.POST.get("uuid")
    
        proc_dict.update_dict(uuid, (True, base64_image))
        
        return HttpResponse("Success", status=200)