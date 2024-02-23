from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey("Topic", on_delete=models.SET_NULL, null=True) 
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=200, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True )
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        ordering = ['-update', '-created']
    def __str__(self):
        return self.name

class Message(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-update']
    def __str__(self):
        return self.body[:50]

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name