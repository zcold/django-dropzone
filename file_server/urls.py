from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = patterns('',
  url(r'^$', 'file_server.views.root'),
  url(r'^admin/', include(admin.site.urls)),
  url(r'^login/$', 'file_server.views.user_login'),
  url(r'^logout/$', 'file_server.views.user_logout'),
  url(r'^file_upload/$', 'file_server.views.file_upload'),
  url(r'^remove_file/[^\s/]+/[^\s/]+\.*[^\s/]+', 'file_server.views.file_remove'),
  url(r'^remove_file_without_uploader/[^\s/]+\.*[^\s/]+', 'file_server.views.file_remove_without_uploader'),
  url(r'^file_upload/list/$', 'file_server.views.file_list_time'),
  url(r'^file_upload/list/name/$', 'file_server.views.file_list_name'),
  url(r'^file_upload/list/time/$', 'file_server.views.file_list_time'),
  url(r'^file_upload/list/uploader/$', 'file_server.views.file_list_uploader'),
  url(r'^files/[^\s/]+/[^\s/]+\.*[^\s/]+', 'file_server.views.file_download'),
  url(r'^assets/[^\s/]+\.*[^\s/]+', 'file_server.views.assets'),
  url(r'^authorize/$', 'file_server.views.authorize'),
)