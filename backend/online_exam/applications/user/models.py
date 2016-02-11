from django.contrib.auth.models import AbstractUser, UserManager
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


class CustomUserManager(UserManager):
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('role', 0)
        return super().create_superuser(username, email, password,
                                        **extra_fields)


class User(AbstractUser):
    role = models.IntegerField(choices=ROLE_CHOICES, default=2)
    display_name = models.CharField(max_length=50, null=True, blank=True)

    objects = CustomUserManager()

    def get_display_name(self):
        return self.display_name

    def is_teacher(self):
        return self.role == 1

    def is_student(self):
        return self.role == 2

    def save(self, *args, **kwargs):
        if not self.display_name:
            self.display_name = self.username
        super().save(*args, **kwargs)

    def __str__(self):
        return self.get_full_name()


class Profile(models.Model):
    user = models.ForeignKey(User)

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    bio = models.TextField()
    birthday = models.DateField()

    address = models.TextField()
    city = models.CharField(max_length=45, blank=True, null=True)
    state = models.CharField(max_length=45, blank=True, null=True)
    country = models.CharField(max_length=45, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()
