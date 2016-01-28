from django.contrib.auth.models import AbstractUser
from django.db import models

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female')
)

ROLE_CHOICES = (
    (0, 'admin'),
    (1, 'teacher'),
    (2, 'student')
)


class User(AbstractUser):
    role = models.IntegerField(choices=ROLE_CHOICES)
    display_name = models.CharField(max_length=50, null=True, blank=True)

    def get_display_name(self):
        return self.display_name

    def save(self, *args, **kwargs):
        if not self.display_name:
            self.display_name = self.username
        super().save(*args, **kwargs)

    def __unicode__(self):
        return self.get_full_name()


class Profile(models.Model):
    user = models.ForeignKey(User)

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    bio = models.TextField()
    birthday = models.DateField()

    address = models.TextField()
    city = models.CharField(max_length=45)
    state = models.CharField(max_length=45)
    country = models.CharField(max_length=45)
    zip_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)

    def __unicode__(self):
        return self.user.get_full_name()
