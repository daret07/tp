from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
  Group,
  AbstractBaseUser,
  BaseUserManager,
  PermissionsMixin
)

class CustomUserManager(BaseUserManager):
  def create_user(self,username,password=None):
    user = self.model(username=username)
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_superuser(self,username,password=None):
    user = self.model(username=username)
    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    user.save(using=self._db)
    return user

class usuario(AbstractBaseUser,PermissionsMixin):

  tTipoLogin = (
    ('password','Password'),
    ('imap','IMAP'),
  )

  username             = models.CharField(max_length=120,verbose_name='Usuario',unique=True)
  first_name           = models.CharField(max_length=45,verbose_name='Nombre (s)')
  last_name            = models.CharField(max_length=45,verbose_name='Apellidos',blank=True,null=True)
  email                = models.EmailField(verbose_name='Email',blank=True,null=True)
  avatar               = models.ImageField(upload_to='avatars/',blank=True,null=True)
  metodo_autenticacion = models.CharField(max_length=10,choices=tTipoLogin,default='password')
  is_staff             = models.BooleanField(default=False)

  objects        = CustomUserManager()
  USERNAME_FIELD = 'username'

  def get_full_name(self):
    return self.username

  def get_short_name(self):
    return self.username

  def __unicode__(self):
    return self.username
  
  def verbose_name(self):
    return self._meta.verbose_name


class perfil(Group):
  pass

class dominio_permitido(models.Model):
  
  tTipos = (
    ('imap4','IMAP4'),
    ('imap4_ssl','IMAP4_SSL'),
  )

  dominio = models.CharField(max_length=120)
  host    = models.CharField(max_length=120)
  puerto  = models.IntegerField()
  tipo    = models.CharField(max_length=5,choices=tTipos,default='imap4')
  activo  = models.BooleanField(default=True)

  def __unicode__(self):
    return self.dominio
