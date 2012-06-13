from django.db import models
import jsonfield

class Counter(models.Model):
    name = models.CharField(max_length=16)
    data = jsonfield.JSONField()

class Update(models.Model):
    counter = models.ForeignKey(Counter)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=True)
