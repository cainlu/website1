from django.conf.urls.defaults import *
from django.contrib import admin
import main.views
import os

admin.autodiscover()

def url_change(request, urls, views):
    params = [url for url in urls.split('/') if url]
    method_name = params[-1]
    method = getattr(views, method_name)
    return method(request)

urlpatterns = patterns('',
	(r'^media/admin/(?P<path>.*)$', 'django.views.static.serve', {'document_root':os.path.join(os.path.dirname(__file__), '../admin')}),
    (r'css/(?P<path>.*)$', 'django.views.static.serve', {'document_root':os.path.join(os.path.dirname(__file__), '../css')}),
    (r'js/(?P<path>.*)$', 'django.views.static.serve', {'document_root':os.path.join(os.path.dirname(__file__), '../js')}),
    (r'video/(?P<path>.*)$', 'django.views.static.serve', {'document_root':os.path.join(os.path.dirname(__file__), '../video')}),
    (r'image/(?P<path>.*)$', 'get_image.views.get_image'),
    (r'^main/(?P<urls>.*)', url_change, {'views':main.views}),
    (r'^$', 'main.views.display'),
	(r'^admin/', include(admin.site.urls)),
)
