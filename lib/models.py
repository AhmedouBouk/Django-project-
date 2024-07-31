from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class LibraryManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(username=username)

class Library(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    name_lib = models.CharField(max_length=60, null=False)
    username = models.CharField(max_length=10, unique=True, null=False)
    email = models.EmailField(max_length=60, unique=True, null=False)
    password = models.CharField(max_length=80, null=False)
    phone_number = models.CharField(max_length=15, null=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    champ_activation = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True, null=True)
    last_login = models.DateTimeField(auto_now=True, null=True)

    objects = LibraryManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'Librairies'



class Livre(models.Model):
    GENRE_CHOICES = [
        ('Action', 'Action'),
        ('Human Development', 'Human development'),
        ('Romance', 'Romance'),
        ('Fiction', 'Fiction'),
    ]

    Id_livre = models.AutoField(primary_key=True)
    Name_book = models.CharField(max_length=50, default=None)
    status= models.CharField(max_length=100,null=True,default='disponible')

    Authour_name = models.CharField(max_length=20, null=True, blank=True)
    Genre = models.CharField(max_length=20, choices=GENRE_CHOICES, null=True, blank=True)
    Image = models.ImageField(upload_to='images/',null=True,blank=True)
    Stock = models.IntegerField(default=1)
    Id_lib = models.ForeignKey(Library, on_delete=models.CASCADE)
    Prix = models.FloatField(default=100)
    Description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'Livres'