from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from models import *

@receiver(post_save, sender=Agent)
def set_agent(sender, instance, **kwargs):
    print "here"
    user_obj = User.objects.filter(username=instance.name).values_list('id', flat=True)
    group_obj = Group.objects.get(name='Agent')
    group_obj.user_set.add(user_obj[0])
    print "successs"


@receiver(post_save, sender=Customer)
def set_customer(sender, instance, **kwargs):
    print "here"
    user_obj = User.objects.filter(username=instance.name).values_list('id', flat=True)
    group_obj = Group.objects.get(name='customer')
    group_obj.user_set.add(user_obj[0])
    print "successs"

@receiver(post_save, sender=Centermanager)
def set_centermanager(sender, instance, **kwargs):
    print "here"
    user_obj = User.objects.filter(username=instance.name).values_list('id', flat=True)
    group_obj = Group.objects.get(name='Center_Manager')
    group_obj.user_set.add(user_obj[0])
    print "successs"


@receiver(post_save, sender=Nextwealthmanager)
def set_nextwealthmanager(sender, instance, **kwargs):
    print "here"
    user_obj = User.objects.filter(username=instance.name).values_list('id', flat=True)
    group_obj = Group.objects.get(name='Nextwealth_Manager')
    group_obj.user_set.add(user_obj[0])
    print "successs"
