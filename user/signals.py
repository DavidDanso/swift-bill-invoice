from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from .models import *
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

def createUser(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            username = user.username,
            email = user.email,
            name = user.first_name,
        )

        # Signal to SEND EMAIL WHEN A NEW USER REGISTERS
        subject = 'Welcome to Swift-Bill'
        template = 'welcome_email.html'
        context = {'user': user}
        message = render_to_string(template, context)
        send_mail(
            subject,
            '',
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
            html_message=message # pass the template as html_message
        )

def updateProfile(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.email = profile.email
        user.username = profile.username
        user.save()

def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()

post_save.connect(createUser, sender=User)
post_save.connect(updateProfile, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)