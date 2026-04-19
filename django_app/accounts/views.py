from django.http import JsonResponse
from django.contrib.auth import authenticate
import jwt
from datetime import datetime, timedelta
import json
from django.views.decorators.csrf import csrf_exempt

SECRET_KEY = "secret"

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        data = json.loads(request.body)

        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            token = jwt.encode({
                "sub": user.username,
                "exp": datetime.utcnow() + timedelta(minutes=30)
            }, SECRET_KEY, algorithm="HS256")

            return JsonResponse({"access_token": token})

        return JsonResponse({"error": "Invalid credentials"}, status=401)