import os.path, logging
from datetime import date

from django.conf import settings
from ipware.ip import get_ip

def prepare_log():
  log_file = os.path.join(settings.LOG_DIR, str(date.today()) + '.log')
  logging.basicConfig(filename=log_file, format = settings.LOG_FORMAT, level=logging.INFO)
  return ''

def log(msg) :
  logging.info(msg)

def format_msg(msg, tail = None):
  return msg + ('.' if not tail else (' ' + tail + '.'))

def valid_user_msg(request, during = None) :
  msg = 'Valid user login: {} from {}'.format(request.user, get_ip(request))
  return format_msg(msg, during)

def invalid_user_msg(request, during = None) :
  msg = 'Invalid user login: {} from {}'.format(request.user, get_ip(request))
  return format_msg(msg, during)

def inactive_user_msg(request, during = None) :
  msg = 'Invalid user login: {} from {}, user is inactive'.format(
    request.user, get_ip(request))
  return format_msg(msg, during)

def bad_user_msg(request, during = None) :
  msg = 'Invalid user login: {} from {}, bad username/password'.format(
    request.user, get_ip(request))
  return format_msg(msg, during)

def bad_request_method_msg(request, during = None) :
  msg = 'Invalid user login from {}, bad request method {}'.format(
    get_ip(request), request.method)
  return format_msg(msg, during)

def file_upload_msg(request, file_name = 'file') :
  msg = 'File upload from {}, file name: {}'.format(get_ip(request), file_name)
  user = 'by user {}'.format(request.user) if request.user else None
  return format_msg(msg, user)

def file_download_msg(request, file_name = 'file') :
  msg = 'File download from {}, file name: {}'.format(get_ip(request), file_name)
  user = 'downloaded by user {}'.format(request.user) if request.user else None
  return format_msg(msg, user)

def cannot_find_file_msg(request, file_name = 'file') :
  msg = 'Cannot find file {}, request from {}'.format(file_name, get_ip(request))
  user = 'requested by user {}'.format(request.user) if request.user else None
  return format_msg(msg, user)

def file_remove_msg(request, file_name = 'file') :
  msg = 'File {} is removed'.format(file_name)
  user = 'by user {} from {}'.format(request.user, get_ip(request)) if request.user else None
  return format_msg(msg, user)