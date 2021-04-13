from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser,BaseUserManager

class AccountManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password,
            is_staff=True,
            is_superuser=True
        )
        user.save(using=self._db)
        return user



class CustomUser(AbstractUser):
    username = None
    uid=models.AutoField(primary_key=True)
    email = models.EmailField('email address',unique=True)
    name = models.CharField('Name', max_length=255, blank=True,
                                  null=False)
    adminPrivilege=models.BooleanField(default=False)
    REQUIRED_FIELDS=[]
    USERNAME_FIELD='email'

    objects = AccountManager()

    def __str__(self):
        return "{}-{}-{}".format(self.email,self.name,self.adminPrivilege)