# usuarios/backends.py
from django.contrib.auth.backends import ModelBackend
from .models import SyncUsuario

class PlainTextAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = SyncUsuario.objects.get(username=username)
            if user.password == password:
                return user
        except SyncUsuario.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return SyncUsuario.objects.get(pk=user_id)
        except SyncUsuario.DoesNotExist:
            return None