import os, os.path, time
from functools import reduce

if 'import django' :
  from django.http import HttpResponse
  from django.shortcuts import render_to_response, redirect
  from django.template import RequestContext
  from django.core.servers.basehttp import FileWrapper
  from django.conf import settings
  from django.template.context_processors import csrf
  from django.contrib.auth import authenticate, login, logout
  from django.contrib.auth.models import User

from .msgs import *

def root(request) :
  return redirect('/file_upload/')

def authorize(request):
  msg = prepare_log()
  if request.method == 'POST':
    username=request.POST.get('username')
    password=request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user :
      if user.is_active:
        login(request, user)
        log(valid_user_msg(request))
        return redirect('/file_upload/')
      msg = inactive_user_msg(request)
    else :
      msg = bad_user_msg(request)
  else :
    msg = bad_request_method_msg(request, 'during user logging in')
  log(msg)
  return HttpResponse(msg)

def user_login(request):
  if request.user.is_authenticated():
    return redirect('/file_upload/')
  return render_to_response('login.html',
    context_instance=RequestContext(request))

def user_logout(request):
  logout(request)
  return redirect('/login/')

def file_upload(request):
  msg = prepare_log()
  if request.user.is_authenticated():
    if request.method == 'POST':
      uploaded_file = request.FILES['file']
      file_name = uploaded_file.name
      user_path = os.path.join(settings.FILE_DIR, request.user.username)
      if not os.path.exists(user_path) :
        os.mkdir(user_path)
      file_path = os.path.join(user_path, file_name)
      with open(file_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
          destination.write(chunk)
      msg = file_upload_msg(request, file_name)
    else :
      msg = bad_request_method_msg(request, 'during file uploading')
    log(msg)
    return render_to_response('file_uploader.html',
      {'user': str(request.user)}, context_instance=RequestContext(request))
  else :
    msg = invalid_user_msg(request, 'during file uploading')
    log(msg)
    return redirect('/login/')

def file_download(request) :
  msg = prepare_log()
  file_name = request.path.split('/files/')[-1]
  user_name = file_name.split('/')[0]
  file_short_name = file_name.split('/')[1]
  file_path = os.path.join(settings.FILE_DIR, file_name)
  if os.path.isfile(file_path) :
    fp = open(file_path, 'rb')
    response = HttpResponse(FileWrapper(fp), content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename={}'.format(file_short_name)
    fp.close()
    msg = file_download_msg(request, file_short_name + ' uploaded by user {}'.format(user_name))
    log(msg)
    return response
  msg = cannot_find_file_msg(request, file_short_name)
  log(msg)
  return HttpResponse(msg)

def assets(request) :
  msg = prepare_log()
  file_name = request.path.split('/assets/')[-1]
  file_path = os.path.join(settings.ASSET_DIR, file_name)
  if os.path.isfile(file_path) :
    fp = open(file_path, 'rb')
    response = HttpResponse(FileWrapper(fp), content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename={}'.format(file_name)
    fp.close()
    msg = file_download_msg(request, file_name + ' as asset')
    log(msg)
    return response
  msg = cannot_find_file_msg(request, file_name)
  log(msg)
  return HttpResponse(msg)

def file_remove_without_uploader(request) :
  msg = prepare_log()
  file_name = request.path.split('/remove_file_without_uploader')[-1]
  user_name = request.user.username
  user_path = os.path.join(settings.FILE_DIR, user_name)
  file_short_name = file_name.split('/')[-1]
  file_path = os.path.join(user_path, file_short_name)
  if os.path.isfile(file_path) :
    os.remove(file_path)
    msg = file_remove_msg(request, file_name)
    return redirect('/file_upload/list/')
  msg = cannot_find_file_msg(request, file_short_name)
  log(msg)
  return HttpResponse(msg)

def file_remove(request) :
  msg = prepare_log()
  file_name = request.path.split('/remove_file/')[-1]
  user_name = file_name.split('/')[0]
  user_path = os.path.join(settings.FILE_DIR, user_name)
  file_short_name = file_name.split('/')[1]
  file_path = os.path.join(user_path, file_short_name)
  if os.path.isfile(file_path) :
    os.remove(file_path)
    msg = file_remove_msg(request, file_name)
    return redirect('/file_upload/list/')
  msg = cannot_find_file_msg(request, file_short_name)
  log(msg)
  return HttpResponse(msg)

def time_string(file_abs_path) :
  return time.strftime('%Y-%m-%d', time.localtime(mtime(file_abs_path)))

def mtime(file_abs_path) :
  return os.path.getmtime(file_abs_path)

def get_all_files() :
  files = []
  index = 0
  for user in User.objects.all() :
    user_file_dir = os.path.join(settings.FILE_DIR, user.username)
    if not os.path.exists(user_file_dir) :
      os.mkdir(user_file_dir)
    file_names = [f for f in os.listdir(user_file_dir)
      if os.path.isfile(os.path.join(user_file_dir, f))]
    file_names.sort(key = lambda f : mtime(os.path.join(user_file_dir, f)))
    for f in file_names :
      file_abs_path = os.path.join(user_file_dir, f)
      files.append({
        'index' : index,
        'date' : time_string(file_abs_path),
        'date_sec': mtime(file_abs_path),
        'download_url' : settings.FILE_URL + user.username + '/' + f,
        'name' : f,
        'uploader' : user.username})
      index += 1
  return files

def sort_file_list(files, key = 'date_sec') :
  for f in files :
    if key in f.keys() :
      files.sort(key = lambda f : f[key])
      for i, f in enumerate(files) :
        f['index'] = i
    return files

def file_list_time(request):
  files = get_all_files()
  files = sort_file_list(files, 'date_sec')
  return render_to_response('file_list.html', {'files' : files})

def file_list_name(request):
  files = get_all_files()
  files = sort_file_list(files, 'name')
  return render_to_response('file_list.html', {'files' : files})

def file_list_uploader(request):
  files = get_all_files()
  files = sort_file_list(files, 'uploader')
  return render_to_response('file_list.html', {'files' : files})