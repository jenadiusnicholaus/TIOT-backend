import os
import sys
import struct
import logging
import django


# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
django.setup()

from django.contrib.auth import authenticate, get_user_model
from django.conf import settings

# Set up logging
log_file_path = os.path.join(settings.BASE_DIR, 'ejabberd_auth_bridge.log')
sys.stderr = open(log_file_path, 'w')
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename=log_file_path,
                    filemode='a')

def from_ejabberd():
    input_length = sys.stdin.buffer.read(2)
    (size,) = struct.unpack('>h', input_length)
    return sys.stdin.read(size).split(':')

def to_ejabberd(bool):
    answer = 0
    if bool:
        answer = 1
    token = struct.pack('>hh', 2, answer)
    sys.stdout.buffer.write(token)
    sys.stdout.flush()

def auth(username, server, password):
    user = authenticate(username=username, password=password)
    if user is None:
        logging.info('Authentication failed for user: %s', username)
    elif not user.is_active:
        logging.info('User is inactive: %s', username)
    return user is not None and user.is_active

def isuser(username, server):
    User = get_user_model()
    return User.objects.filter(username=username).exists()

def setpass(username, server, password):
    User = get_user_model()
    try:
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        return True
    except User.DoesNotExist:
        return False

while True:
    data = from_ejabberd()
    success = False
    if data[0] == "auth":
        success = auth(data[1], data[2], data[3])
        logging.info("Auth success: " + str(success))
    elif data[0] == "isuser":
        success = isuser(data[1], data[2])
        logging.info("Isuser success: " + str(success))
    elif data[0] == "setpass":
        success = setpass(data[1], data[2], data[3])
    to_ejabberd(success)