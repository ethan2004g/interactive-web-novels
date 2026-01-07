"""Debug token to see the payload"""
import sys
from jose import jwt
from app.core.config import settings

if len(sys.argv) < 2:
    print("Usage: python debug_token.py <token>")
    sys.exit(1)

token = sys.argv[1]

try:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    print("Token payload:")
    for key, value in payload.items():
        print(f"  {key}: {value} (type: {type(value).__name__})")
except Exception as e:
    print(f"Error decoding token: {e}")

