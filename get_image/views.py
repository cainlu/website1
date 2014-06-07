#coding=utf-8
from django.http import HttpResponse
from PIL import Image
import StringIO
import os

def get_image(request, path):
    mode = request.GET.get('mode', '0')#0为原图，1为缩略图
    image_type = path.split('.')[-1].lower()
    image_type = image_type.replace('jpg', 'jpeg')
    io = StringIO.StringIO()
    path = os.path.join(os.path.dirname(__file__), '../image/' + path)
    if mode == '1':
        image = Image.open(path)
        width = image.size[0]
        height = image.size[1]
        if width > 300:
            times = width / 300.0
            width = width / times
            height = height / times
            height = max(height, 60)
            image = image.resize((int(width), int(height)), Image.ANTIALIAS)
        if height > 300:
            times = height / 300.0
            width = width / times
            width = max(width, 60)
            height = height / times
            image = image.resize((int(width), int(height)), Image.ANTIALIAS)
        image.save(io, image_type)
        return HttpResponse(io.getvalue(), mimetype = 'image/' + image_type)
    elif mode == '0':
        if path.endswith('.gif') or path.endswith('.ico'):
            image = open(path, 'rb').read()
            return HttpResponse(image, mimetype = 'image/' + image_type)
        else:
            image = Image.open(path)
            width = image.size[0]
            height = image.size[1]
            if width > 580:
                times = width / 580.0
                width = width / times
                height = height / times
                image = image.resize((int(width), int(height)), Image.ANTIALIAS)
            image.save(io, image_type)
            return HttpResponse(io.getvalue(), mimetype = 'image/' + image_type)