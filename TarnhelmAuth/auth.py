from TarnhelmAuth.models import LoginToken, RegisteredUser, gen_uid

class User:
    def __init__(self, uid, name=None, admin=False):
        self.uid = uid;
        self.name = name;
        self.admin = False;
    
    def is_anonymous(self):
        return (self.name is None) or self.admin;

class InvalidPasswordException(Exception):
    def __init__(self, value):
        self.value = value;
    def __str__(self):
        return repr(self.value);

def anonymous_login(request):
    login = LoginToken(is_anonymous = True);
    login.full_clean();
    login.save();
    request.session["lt"] = login.id;

def registered_login(request, username, password):
    """
    Logins in a user with the specified username and password. If the login succedes, a user object will be available in request.user. 
    
    Params:
        request:    HTTPRequest object
        username:   A string representing a username
        password:   A string represnting a password
    
    Throws:
        RegisteredUser.DoesNotExist:    If the specified username could not be found
        InvalidPasswordException:       If the password provides is invalid
    """
    user = RegisteredUser.objects.get(name=username);
        
    if user.verify_password(password):
        login = LoginToken(uid = user.uid, is_anonymous = False);
        login.full_clean();
        login.save();
        request.session["lt"] = login.id;
    else:
        raise InvalidPasswordException("Invalid Password for " + user.name);

def register_user(username, password, is_admin=False):
    """
    Creates a new user with the specified username and password
    
    Params:
        username:   The name of the user
        password:   The password of the user
        is_admin:   True if the specified user is an administrator
    
    """
    user = RegisteredUser.create(username, password);
    user.is_admin = is_admin;
    user.full_clean();
    user.save();