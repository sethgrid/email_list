from django.db import models

# Create your models here.

class Email(models.Model):
    email_address = models.CharField(max_length=80)

    def __unicode__(self):
        return self.email_address

class Sender(models.Model):
    name = models.CharField(max_length=4)

    def __unicode__(self):
        return self.name

class List(models.Model):
    sender = models.ForeignKey(Sender)
    recipient = models.ForeignKey(Email)
    unsubscribed = models.IntegerField(default=0)

