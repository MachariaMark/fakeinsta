from django.db import models
from django.contrib.auth.models import User
import datetime as dt
from pyuploadcare.dj.models import ImageField
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

#Profile model
class Profile(models.Model):
  prof_pic = ImageField(blank=True, manual_crop="")
  bio = models.CharField(max_length = 200)
  user = models.OneToOneField('auth.User',on_delete=models.CASCADE, default=None)
    
  def save_profile(self):
    self.save()
            
  def update_profile(self):
    prof=Profile.objects.filter(id=Profile.id).update()
        
  def delete_image(self):
    prof=Profile.objects.filter(id=Profile.id).delete()
        
    
  @classmethod
  def profile(cls):
    profile = cls.objects.filter(id=Profile.id)
    return profile
    
  def __str__(self):
    return str(self.user)

@receiver(post_save,sender=User)
def create_profile(sender, instance,created,**kwargs):
  if created:
    Profile.objects.create(user=instance)
        
@receiver(post_save,sender=User)
def save_profile(sender, instance,**kwargs):
  instance.profile.save()