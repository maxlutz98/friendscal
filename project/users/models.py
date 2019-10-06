from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core import validators
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, username, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        if not first_name or not last_name:
            raise ValueError('Users must have a name')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Angepasster Nutzer mit E-Mail als Anmeldeinformation.
    """
    email = models.EmailField(_('E-Mail Addresse'), unique=True)
    first_name = models.CharField(_('Vorname'), max_length=150)
    last_name = models.CharField(_('Nachname'), max_length=150)
    shares = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='shared_by', blank=True,
                                    verbose_name=_('Freigaben'),
                                    help_text='Nutzer, die deinen Kalender einsehen dürfen.')
    invitations = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='invited', verbose_name=_(''))
    username = models.CharField(_('Nutzername'), unique=True, max_length=150,
                                help_text=_('Nur Buchstaben, Zahlen und @/./+/-/_ .'),
                                validators=[
                                    validators.RegexValidator(r'^[\w.@+-]+$', _('Gib einen gültigen Nutzernamen ein.'),
                                                              'invalid')])
    avatar = models.ImageField(_('Profilbild'), upload_to='avatars', default='avatars/default-avatar.png')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.get_full_name()

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
