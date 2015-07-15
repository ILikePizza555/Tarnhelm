from django.db import models
from django.conf import settings
import hashlib
import os

#helper functions
def gen_uid():
    """
    Generates a random user id
    """
    m = hashlib.sha1();
    m.update(os.urandom(5));
    return m.hexdigest();

#Models
class RegisteredUser(models.Model):
    """
    Describes a registered user.
    """
    uid = models.CharField(max_length=40, blank=False, unique=True, default=gen_uid);
    name = models.CharField(max_length=settings.TARNHELM_USERNAME_LENGTH, unique=True);
    password_hash = models.CharField(max_length=40);
    password_salt = models.CharField(max_length=6, blank=False);
    
    #Misceleneous info
    rank = models.PositiveIntegerField(default=0);
    admin = models.BooleanField(default=False);
    
    def verify_password(self, password):
        if(hashlib.sha1(password + self.password_salt).hexdigest() == self.password_hash):
            return True;
        else:
            return False;
    
    @classmethod
    def create(cls, username, password):
        salt = hashlib.sha1(os.urandom(1)).hexdigest()[:6]
        return cls(name = username, password_salt = salt, password_hash = hashlib.sha1(password + salt).hexdigest());
        
    def __unicode__(self):
        return "User [" + self.name + "]: UID: " + self.uid;

class LoginToken(models.Model):
    """
    Describes a login token.
    """
    uid = models.CharField(max_length=40, blank=False, default=gen_uid);
    is_anonymous = models.BooleanField(default=True);
    time = models.DateTimeField(auto_now_add=True);