from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.conf import settings
from django.utils.text import slugify

from typing import Iterable, Optional


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_field):
        if not email:
            raise ValueError("email은 꼭 있어야함")
        user = self.model(email=self.normalize_email(email), **extra_field)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_field):
        user = self.create_user(email, password, **extra_field)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email


class TimeStampedModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = False


class Camping(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="camping"
    )
    title = models.CharField(max_length=255)
    review = models.TextField()
    tags = models.ManyToManyField("CampingTag", related_name="camping")

    def __str__(self):
        return self.title


class Blog(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="blog"
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    tags = models.ManyToManyField("BlogTag", related_name="blog")

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title


class TagModel(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True)

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: Optional[str] = None,
        update_fields: Optional[Iterable[str]] = None,
    ) -> None:
        self.slug = slugify(self.name, allow_unicode=True)
        return super().save(force_insert, force_update, using, update_fields)

    class Meta:
        abstract = False

    def __str__(self):
        return self.name


class BlogTag(TagModel):
    pass


class CampingTag(TagModel):
    pass
