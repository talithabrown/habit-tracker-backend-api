from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager, make_password, apps
from django.db.models import Q
from datetime import date
from pprint import pprint

# Create your models here.

class CustomUserManager(UserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        #if not username:
            #raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        username = email
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    objects = CustomUserManager()
    email = models.EmailField(max_length=255, unique=True)


class Habit(models.Model):
    habit = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')

class HabitCompleteDate(models.Model):
    complete_date = models.DateField(default=date.today)
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='habit_complete_dates')