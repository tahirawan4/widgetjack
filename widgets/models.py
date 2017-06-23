import os

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.utils import timezone


class User(AbstractUser):
    background = models.ForeignKey('BackgroundImages', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return 'First Name: {}, Email: {}'.format(self.first_name, self.email)


class Widget(models.Model):
    name = models.CharField(max_length=200)
    link = models.CharField(max_length=500)
    is_featured= models.BooleanField(default=False)
    icon = models.ImageField(upload_to='images/widget/icons', blank=True,
                               null=True, default='images/widget/icons/missing_icon.png')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Name: {}, Featured: {}'.format(self.name, self.is_featured)


class BackgroundImages(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/widget/backgrounds', blank=True, null=True, default='')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Name: {}'.format(self.name)


class UsersWidgets(models.Model):
    user = models.ForeignKey('User')
    widget = models.ForeignKey('Widget')
    click_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)


@receiver(models.signals.post_delete, sender=Widget)
def auto_delete_icon_on_delete(sender, instance, **kwargs):
    """
    Deletes Icon from filesystem
    when corresponding `User` object is deleted.
    """
    if instance.icon:
        delete_if_file_exist(instance.icon.path)


@receiver(models.signals.pre_save, sender=Widget)
def auto_delete_icon_on_change(sender, instance, **kwargs):
    """
    Deletes old Icon from filesystem when corresponding
    `icon` object is updated with new Icon.
    """
    if not instance.pk:
        return False

    try:
        old_icon = Widget.objects.get(pk=instance.pk).icon
    except Widget.DoesNotExist:
        return False

    new_icon = instance.icon
    if not old_icon == new_icon:
        delete_if_file_exist(old_icon.path)


@receiver(models.signals.post_delete, sender=BackgroundImages)
def auto_delete_image_on_delete(sender, instance, **kwargs):
    """
    Deletes Image from filesystem
    when corresponding `User` object is deleted.
    """
    if instance.image:
        delete_if_file_exist(instance.image.path)


@receiver(models.signals.pre_save, sender=BackgroundImages)
def auto_delete_image_on_change(sender, instance, **kwargs):
    """
    Deletes old Image from filesystem when corresponding
    `image` object is updated with new Image.
    """
    if not instance.pk:
        return False

    try:
        old_image = Widget.objects.get(pk=instance.pk).image
    except Widget.DoesNotExist:
        return False

    new_image = instance.image
    if not old_image == new_image:
        delete_if_file_exist(old_image.path)


def delete_if_file_exist(file_path):
    if os.path.isfile(file_path):
        try:
            os.remove(file_path)
        except OSError:
            pass
