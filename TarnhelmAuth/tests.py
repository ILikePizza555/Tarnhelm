from django.test import TestCase, RequestFactory
from TarnhelmAuth.models import RegisteredUser
from TarnhelmAuth.auth import anonymous_login, registered_login
from TarnhelmAuth.middleware import TarnhelmAuthMiddleware
import hashlib
from django.contrib.sessions.middleware import SessionMiddleware

def gen_request_with_session(factory):
    session_middleware = SessionMiddleware();
    request = factory.get('/auth/test');
    
    session_middleware.process_request(request);
    request.session.save();
    
    return request;

# Create your tests here.
class ModelAuthTestCase(TestCase):
    user1_pass = "bbb";
    user2_pass = "fff";
    
    def setUp(self):
        self.user1 = RegisteredUser.create("aaa", self.user1_pass);
        self.user2 = RegisteredUser.create("ggg", self.user2_pass);
    
        self.user1.full_clean();
        self.user2.full_clean();
        self.user1.save();
        self.user2.save();
    
    def tearDown(self):
        self.user1.delete();
        self.user2.delete();
    
    def test_hash(self):
        user1_test_hash = hashlib.sha1(self.user1_pass + self.user1.password_salt).hexdigest();
        self.assertTrue(user1_test_hash == self.user1.password_hash);
        
        user2_test_hash = hashlib.sha1(self.user2_pass + self.user2.password_salt).hexdigest();
        self.assertTrue(user2_test_hash == self.user2.password_hash);
    
    def test_verify_password(self):
        self.assertTrue(self.user1.verify_password(self.user1_pass));
        self.assertTrue(self.user2.verify_password(self.user2_pass));

class MiddleWareAuthTestCase(TestCase):
    r_user_pass = "hello";
    
    def setUp(self):
        self.r_user = RegisteredUser.create("r_user", self.r_user_pass);
        
        self.r_user.full_clean();
        self.r_user.save();
        
        self.r_user_id = self.r_user.uid;
        
        #Request factory
        self.factory = RequestFactory();
    
    def test_anonymous_login(self):
        request = gen_request_with_session(self.factory);
        
        anonymous_login(request);
        
        #Login token should not be empty
        self.assertNotEqual(request.session.get('lt'), None);
        
        auth_middleware = TarnhelmAuthMiddleware();
        auth_middleware.process_request(request);
        
        self.assertNotEqual(request.user, None);
        self.assertTrue(request.user.is_anonymous());
        self.assertEqual(request.user.name, None);
        self.assertNotEqual(request.user.uid, None);
        
    def test_registered_login(self):
        request = gen_request_with_session(self.factory);
        auth_middleware = TarnhelmAuthMiddleware();
        
        registered_login(request, "r_user", self.r_user_pass);
        
        #Login token should not be empty
        self.assertNotEqual(request.session.get('lt'), None);
        
        auth_middleware.process_request(request);
        
        self.assertNotEqual(request.user, None);
        self.assertFalse(request.user.is_anonymous());
        self.assertEqual(request.user.name, "r_user");
        self.assertEqual(request.user.uid, self.r_user_id);
        
    def test_login_fail(self):
        request = gen_request_with_session(self.factory);
        auth_middleware = TarnhelmAuthMiddleware();
        
        self.assertRaises(RegisteredUser.DoesNotExist, registered_login, request, "fake_user", "aaaaa");
        self.assertEqual(request.session.get('lt'), None);
        
        auth_middleware.process_request(request);
        
        self.assertEqual(request.user, None);