from django.contrib.auth.models import User
from django.contrib.auth import get_user_model,backends
from imaplib import IMAP4

class autenticar(backends.ModelBackend):
  def authenticate(self,username=None,password=None):
    """
    try:
      c = IMAP4('')
      c.login(username,password)
      c.logout()
    except:
      return None
    """

    user_model = get_user_model()
    user = None

    try:
      user = user_model.objects.get(username=username)
      if not user.check_password(password):
        user = None
    except User.DoesNotExist:
      pass
    
    return user
    
  def get_user(self,user_id):
    
    user_model = get_user_model()

    try:
      return user_model.objects.get(pk=user_id)
    except:
      return None
