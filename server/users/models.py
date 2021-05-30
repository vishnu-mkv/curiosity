import datetime

from PIL import Image
from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from .manager import UserManager


# Create your models here.


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, verbose_name='email address', max_length=255)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)  # True on email activation
    writer = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'first_name', 'last_name']

    def get_full_name(self):
        return str(self.first_name + ' ' + self.last_name)

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    @property
    def is_writer(self):
        return self.writer


class WriterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=50, blank=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name() + " - Writer Profile"


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.get_full_name()} - Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # resizing image to 320*320
        img = Image.open(self.profile_pic.path)
        if img.height > 320 or img.width > 320:
            output_size = (320, 320)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)


class WriterApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    approved = models.BooleanField(null=True)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='Approved_by', blank=True)
    bio = models.TextField(max_length=1000, blank=True)
    writings = models.CharField(max_length=200, blank=True)
    submitted_on = models.DateTimeField(auto_now_add=True)

    def save(self, **kwargs):
        # if user is already a writer
        # do nothing with the application
        if self.user.writer:
            return None
        super(WriterApplication, self).save()

    def __str__(self):
        return self.user.get_full_name() + " - Writer Application"


class EmailActivation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(unique=True, max_length=20)
    generated_on = models.DateTimeField(auto_now_add=True)
    validity = models.IntegerField(default=7)
    activated = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.email} - Email Activation'

    def is_valid(self):
        now = datetime.datetime.now()
        max_validity = self.generated_on + datetime.timedelta(days=self.validity)
        print(now, max_validity, now <= max_validity)
        return now <= max_validity

    def activate_user(self):
        if self.user.active:
            return
        if not self.is_valid():
            return False
        self.activated = True
        self.save()
        return True

    def save(self, *args, **kwargs):
        # if user is active no email activation is created
        if self.user.active:
            return None
        super(EmailActivation, self).save(*args, **kwargs)


def validate_key_and_activate_user(key):
    response = {'status': False, 'message': 'unknown error'}

    try:
        obj = EmailActivation.objects.get(key=key)
        if obj.user.active:
            response['message'] = 'User already active'
            return response
        if not obj.is_valid():
            response['message'] = 'Key expired'

        obj.activated = True
        obj.save()
        response['message'] = 'success'
        response['status'] = True

    except EmailActivation.DoesNotExist:
        response['message'] = 'Invalid Key'

    return response
