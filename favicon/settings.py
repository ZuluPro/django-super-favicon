import os
from django.conf import settings


STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          '/static/')
