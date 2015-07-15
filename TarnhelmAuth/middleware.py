from TarnhelmAuth.auth import User
from TarnhelmAuth.models import RegisteredUser, LoginToken

class TarnhelmAuthMiddleware():
    def process_request(self, request):
        lt = request.session.get("lt");
        
        if lt != None:
            #Get the login token
            token = LoginToken.objects.get(id=lt);
            
            if token.is_anonymous:
                request.user = User(token.uid)
            else:
                #A little bit more work
                r_user = RegisteredUser.objects.get(uid=token.uid);
                request.user = User(uid=r_user.uid, name = r_user.name, admin=r_user.admin);
        else:
            request.user = None;