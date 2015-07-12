from django.db import models
from django.conf import settings
import hashlib
import os

#helper functions
def gen_uid():
    m = hashlib.sha1();
    m.update(os.urandom(5));
    return m.hexdigest();

#Models
class RegisteredUser(models.Model):
    """
    Describes a registered user.
    """
    uid = models.CharField(max_length=40, blank=False, unique=True, default=gen_uid);
    nick = models.CharField(max_length=settings.TARNHELM_USERNAME_LENGTH, unique=True);
    password_hash = models.CharField(max_length=40);
    password_salt = models.CharField(max_length=6);
    
    #Misceleneous info
    rank = models.PositiveIntegerField(default=0);
    admin = models.BooleanField(default=False);
    
    def verify_password(self, password):
        if(hashlib.sha1(password + self.password_salt).hexdigest == self.password_hash) :
            return True
        return False