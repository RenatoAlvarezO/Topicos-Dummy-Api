from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.db.models.fields.files import ImageField
from django.db import models
from django.db.models.fields import (
    AutoField,
    BooleanField,
    CharField,
    IntegerField,
    TextField,
    TimeField,
    DateTimeField
)

class Session(models.Model):
    id = AutoField(primary_key=True)
    facebook_id = IntegerField()
    session_id = CharField(max_length = 255)

