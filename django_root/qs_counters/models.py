from django.db import models

# TODO: add users

class Counter(models.Model):
    COUNT = 0
    DURATION = 1
    name = models.CharField(max_length=64)
    type = models.IntegerField()

class Goal(models.Model):
    counter = models.ForeignKey(Counter)
    target = models.IntegerField()

class Update(models.Model):
    counter = models.ForeignKey(Counter)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=True)
