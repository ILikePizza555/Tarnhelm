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
    '''
    Describes a registered user.
    '''
    #Current UID
    uid = models.CharField(max_length=40, blank=False, unique=True, default=gen_uid);
    #Previous UIDs
    p1_uid = models.CharField(max_length=40);
    p2_uid = models.CharField(max_length=40);
    p3_uid = models.CharField(max_length=40);
    
    #Current nickname
    nick = models.CharField(max_length=settings.TARNHELM_USERNAME_LENGTH, unique=True);
    #Previous nicknames
    p1_name = models.TextField();
    p2_name = models.TextField();
    p3_name = models.TextField();
    
    #Misceleneous info
    rank = models.PositiveIntegerField(default=0);
    admin = models.BooleanField(default=False);