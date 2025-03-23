import jwt

JWT_SECRET = 'shhhhh'

def fetch_user(request, response, next):
    # Get the user from the jwt token and add id to req object
    token = request.headers.get('auth-token')
    if not token:
        return response.status(401).json({"error": "Please authenticate using a valid token"})
    
    try:
        data = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        request.user = data.get('user')
        return next()
    except Exception:
        return response.status(401).json({"error": "Please authenticate using a valid token"})
