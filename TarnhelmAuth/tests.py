from django.test import TestCase
from TarnhelmAuth.models import RegisteredUser
import TarnhelmAuth.auth
import hashlib

# Create your tests here.
class AuthTestCase(TestCase):
    user1_pass = "bbb";
    user2_pass = "fff";
    
    def setUp(self):
        user1 = RegisteredUser.create("aaa", self.user1_pass);
        user2 = RegisteredUser.create("ggg", self.user2_pass);
        
        user1.full_clean();
        user2.full_clean();
        user1.save();
        user2.save();
    
    def tearDown(self):
        RegisteredUser.objects.get(name="aaa").delete();
        RegisteredUser.objects.get(name="ggg").delete();
    
    def test_hash(self):
        user1 = RegisteredUser.objects.get(name="aaa");
        user2 = RegisteredUser.objects.get(name="ggg");
        
        user1_test_hash = hashlib.sha1(self.user1_pass + user1.password_salt).hexdigest();
        self.assertTrue(user1_test_hash == user1.password_hash);
        
        user2_test_hash = hashlib.sha1(self.user2_pass + user2.password_salt).hexdigest();
        self.assertTrue(user2_test_hash == user2.password_hash);
    
    def test_verify_password(self):
        user1 = RegisteredUser.objects.get(name="aaa");
        user2 = RegisteredUser.objects.get(name="ggg");
        
        self.assertTrue(user1.verify_password(self.user1_pass));
        self.assertTrue(user2.verify_password(self.user2_pass));