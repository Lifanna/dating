from django.db import models
from django.contrib.auth.models import AbstractUser, User, BaseUserManager
from . import constants as const


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, aituUserId, password, **extra_fields):        
        user = self.model(aituUserId=aituUserId, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_user(self, aituUserId, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(aituUserId, password, **extra_fields)

    def create_superuser(self, aituUserId, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(aituUserId, password, **extra_fields)

    def is_unique_aituUserId(self, user):
        if user.id is not None and user.aituUserId != "" and self.filter(aituUserId=user.aituUserId).exclude(pk=user.pk).exists():
            return False
        return True


class User(AbstractUser):
    username = None
    email = models.EmailField(('Email address'), blank=True)
    aituUserId = models.CharField("AituUserId", unique=True, max_length=300)
    USERNAME_FIELD = 'aituUserId'

    objects = UserManager()

    class Meta:
        db_table = "auth_user"
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def clean(self):
        # here we can check some mandatory fields and complex relations between fields
        super(User, self).clean()

    def save(self, *args, **kwargs):
        self.clean()
        self.validate_unique()
        super(User, self).save(*args, **kwargs)

    def validate_unique(self, *args, **kwargs):
        super(User, self).validate_unique(*args, **kwargs)
        if not User.objects.is_unique_aituUserId(self):
            raise ValidationError("Пользователь уже существует")


class City(models.Model):
    name = models.CharField(max_length=30, blank=True)

    is_deleted = models.BooleanField(default=False)


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)

    gender = models.CharField("Gender", max_length=1, choices=const.GENDER, blank=True, default="")

    city = models.ForeignKey(City, on_delete=models.CASCADE)

    birth_date = models.DateField("Date of birth", blank=True, null=True)

    avatar = models.ImageField(upload_to='content', blank=True, null=True, default="content/Aaron_Eckhart_0001.jpg")

    latitude = models.FloatField("Latitude", blank=True, null=True)

    longitude = models.FloatField("Longitude", blank=True, null=True)

    breefly = models.TextField("Breefly")

    is_deleted = models.BooleanField(default=False)


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    user_id = models.IntegerField("Was liked User")

    total = models.IntegerField("Total number of likes")

    class Meta:
        unique_together = ('author', 'user_id',)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    user_id = models.IntegerField("Was commented User")
    
    comment_text = models.TextField("Comment text")
    
    comment_date = models.DateTimeField("Comment datetime")
    
    class Meta:
        unique_together = ('author', 'user_id',)


class Dating(models.Model):
    pass
