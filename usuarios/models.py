from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model 


# Create your models here.
class SyncUsuarioManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('O campo de nome de usuário é obrigatório')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)

class SyncUsuario(AbstractBaseUser, PermissionsMixin):


    username = models.CharField(max_length=150, unique=True, primary_key=True)

    name = models.CharField(max_length=150, blank=True)
    password = models.CharField(max_length=128)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    last_login = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    objects = SyncUsuarioManager()

    groups = None
    user_permissions = None

    class Meta:
        managed = True
        db_table = 'sync_usuario'

    def __str__(self):
        return self.username

class Associado(models.Model):
    nome = models.CharField(max_length=255)
    status = models.CharField(max_length=20, default='ATIVO')

    class Meta:
        db_table = 'cadastro_associado'  
        managed = False  
        verbose_name = "Associado"

    def __str__(self):
        return self.nome

class PerfilUsuario(models.Model):
    # MUDANÇA 2: Usar settings.AUTH_USER_MODEL em vez de User
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='perfil'
    )
    eh_comprador = models.BooleanField(default=False, verbose_name="É Comprador?")

    def __str__(self):
        return f"Perfil de {self.user.username}"



User = get_user_model()
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def criar_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        # Se o usuário acabou de ser criado, cria o perfil
        PerfilUsuario.objects.get_or_create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def salvar_perfil_usuario(sender, instance, **kwargs):
    # Tenta acessar o perfil de forma segura
    try:
        instance.perfil.save()
    except PerfilUsuario.DoesNotExist:
        # OPA! Se não tem perfil (usuário antigo), cria um agora.
        PerfilUsuario.objects.create(user=instance)