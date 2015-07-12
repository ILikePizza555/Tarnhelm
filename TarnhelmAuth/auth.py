from TarnhelmAuth.models import AnonymousUser, RegisteredUser, gen_uid

class User:
    def __init__(self, uid, nick=None, admin=False):
        self.uid = uid;
        self.nick = nick;
        self.admin = False;
    
    def is_anonymous(self):
        return (self.nick is None) or self.admin;

class InvalidPasswordException(Exception):
    def __init__(self, value):
        self.value = value;
    def __str__(self):
        return repr(self.value);

def anonymous_login(request):
    request.session["auth"] = User(gen_uid())

def registered_login(request, username, password):
    """
    Logins in a user with the specified username and password.
    
    Params:
        request:    HTTPRequest object
        username:   A string representing a username
        password:   A string represnting a password
    
    Throws:
        RegisteredUser.DoesNotExist:    If the specified username could not be found
        InvalidPasswordException:       If the password provides is invalid
    """
    user = RegisteredUser.objects.get(nick=username);
        
    if user.verify_password(password):
        request.session["auth"] = User(user.uid, user.nick, user.admin);
    else:
        raise InvalidPasswordException("Invalid Password for " + user.name);
        