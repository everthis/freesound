from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import smart_unicode
import uuid

def generate_key():
    return str(uuid.uuid4()).replace('-','')

STATUS_CHOICES = (('approved', 'Approved'),
                  ('rejected', 'Rejected'),
                  ('revoked', 'Revoked'),
                  ('pending', 'Pending'))
DEFAULT_STATUS = 'approved'

class ApiKey(models.Model):
    key            = models.CharField(max_length=32, default=generate_key, db_index=True, unique=True)
    user           = models.ForeignKey(User, related_name='api_keys')
    status         = models.CharField(max_length=32, default=DEFAULT_STATUS, choices=STATUS_CHOICES)
    name           = models.CharField(max_length=64)
    url            = models.URLField()
    description    = models.TextField(blank=True)
