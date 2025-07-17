from django.db import models
from django.utils.text import slugify
from account.models import Profile

# Create your models here.
class Visit(models.Model):
    country = models.CharField(max_length=255)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="visits")
    slug = models.SlugField(unique=True, blank=True, null=True)
    date_from = models.DateField(blank=True, null=True)
    date_until = models.DateField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Prepopulates the slug field
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.country}-{self.profile.user.username}")
            slug = base_slug
            counter = 1

            while Visit.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.country} by {self.profile.user.username}"