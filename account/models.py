from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.text import slugify

# Create your models here.
def user_directory_path(instance, filename):
    return 'users/avatars/{0}/{1}'.format(instance.user.id, filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)
    avatar = models.ImageField(upload_to=user_directory_path, default="users/avatar.jpg")
    bio = models.TextField(blank=True, max_length=500)
    friends = models.ManyToManyField(User, blank=True, related_name="friends", symmetrical=True)

    # Prepopulates the slug field
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)