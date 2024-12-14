import jwt
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from channels.db import database_sync_to_async
from urllib.parse import parse_qs

User = get_user_model()

@database_sync_to_async
def get_user_from_token(token):
    if not token:
        return AnonymousUser()
    
    try:
        # Decode the token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        
        # Validate and retrieve user
        if not user_id:
            return AnonymousUser()
        
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return AnonymousUser()
    
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return AnonymousUser()

class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        # Extract token from query string or headers
        headers = dict(scope.get("headers", []))
        query_string = scope.get("query_string", b"").decode("utf-8")
        
        # Parse query parameters
        query_params = parse_qs(query_string)
        token = None

        # Try to get token from query parameters
        if 'token' in query_params:
            token = query_params['token'][0]
        
        # If no token in query params, check Authorization header
        if not token and b"authorization" in headers:
            auth_header = headers[b"authorization"].decode("utf-8")
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
        
        # Get user from token
        scope['user'] = await get_user_from_token(token)
        
        # Call the inner application
        return await self.inner(scope, receive, send)

def JWTAuthMiddlewareStack(inner):
    return JWTAuthMiddleware(inner)