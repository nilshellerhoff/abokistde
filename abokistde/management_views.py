import base64
import os

from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.core.management import CommandError
from django.http import HttpResponse
import django.core.management
from datetime import datetime

from functools import wraps

def basicauth(view, realm=""):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        # See if they provided login credentials
        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2:
                if auth[0].lower() == "basic":
                    decoded = base64.b64decode(auth[1]).decode('utf-8')
                    username, password = decoded.split(":")
                    target_user = os.getenv('DJANGO_SUPERUSER_USERNAME')
                    target_password_hash = os.getenv('DJANGO_SUPERUSER_PASSWORD_HASH')

                    if username == target_user:
                        if check_password(password, target_password_hash):
                            return view(request, *args, **kwargs)

        # Either they did not provide an authorization header or
        # something in the authorization attempt failed. Send a 401
        # back to them to ask them to authenticate.

        response = HttpResponse()
        response.status_code = 401
        response['WWW-Authenticate'] = 'Basic realm="%s"' % realm
        return response

    return wrapper


@basicauth
def migrate_view(request):
    return HttpResponse(migrate())


def migrate():
    out_str = ""
    out_str += str(datetime.now()) + " running migrate<br>"
    django.core.management.execute_from_command_line(['manage.py', 'migrate'])
    out_str += str(datetime.now()) + " migrate finished<br>"
    return out_str


@basicauth
def collectstatic_view(request):
    return HttpResponse(collectstatic())


def collectstatic():
    out_str = ""
    out_str += str(datetime.now()) + " running collectstatic<br>"
    django.core.management.execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
    out_str += str(datetime.now()) + " collectstatic finished<br>"
    return out_str


@basicauth
def createsuperuser_view(request):
    return HttpResponse(createsuperuser())


def createsuperuser():
    out_str = ""

    out_str += str(datetime.now()) + " running createsuperuser<br>"

    user, _ = User.objects.get_or_create(username=os.getenv('DJANGO_SUPERUSER_USERNAME'))
    user.email = os.getenv('DJANGO_SUPERUSER_EMAIL')
    user.is_superuser = True
    user.is_staff = True
    user.password = os.getenv('DJANGO_SUPERUSER_PASSWORD_HASH')
    user.save()
    out_str += str(datetime.now()) + " superuser created or updated<br>"

    return out_str
