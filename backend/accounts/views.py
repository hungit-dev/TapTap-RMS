from . import firebase
from firebase_admin import auth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import UserSerializer

# Customer Register View
class CreateCustomerView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        # Get Firebase token from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return Response(
                {"error": "Authorization header is required"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        try:
            # Authorization: Bearer <token>
            token = auth_header.split(" ")[1]
            # Verify Firebase token
            decoded_token = auth.verify_id_token(token)
            # Get information from verified Firebase token
            firebase_uid = decoded_token["uid"]
            email = decoded_token.get("email")
        except Exception:
            return Response(
            {"error": "Invalid Firebase token"},
            status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Get information sent by frontend
        name = request.data.get("name")
        phone = request.data.get("phone", "")
        if not name:
            return Response(
                {"error": "Name is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if Django user already exists
        user = User.objects.filter(
            firebase_uid=firebase_uid
        ).first()
        if user:
            return Response(
                {
                    "error": "User already exists",
                    "user": UserSerializer(user).data
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create Django customer user
        user = User.objects.create(
            firebase_uid=firebase_uid,
            email=email,
            name=name,
            phone=phone,
            role="CUSTOMER",
        )

        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )



# Employee Register View
class CreateEmployeeView(APIView):
    def post(self, request):
        # only manager can create employee account
        if request.user.role != "MANAGER":
            return Response(
                {"error": "Manager access required"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get information sent by frontend
        name = request.data.get("name")
        email = request.data.get("email")
        phone = request.data.get("phone", "")
        role = request.data.get("role")
        if not name or not email or not role:
            return Response(
                {"error": "Name, email, and role are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        allowed_roles = ["SERVER", "KITCHEN", "DRIVER"]
        if role not in allowed_roles:
            return Response(
                {"error": "Invalid employee role"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if Django user already exists
        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "User with this email already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
       # Create Firebase employee account
        firebase_user = auth.create_user(
            email=email,
            display_name=name,
            )
        
        # Create Django employee user
        user = User.objects.create(
            firebase_uid=firebase_user.uid,
            email=email,
            name=name,
            phone=phone,
            role=role,
        )

        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )
