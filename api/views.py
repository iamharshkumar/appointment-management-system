from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from api.models import User_status, Customer
from api.serializers import *


class Signup(APIView):

    def post(self, request):
        f = request.data.get('fname')
        l = request.data.get('lname')
        u = request.data.get('uname')
        i = request.data.get('image')
        p = request.data.get('pwd')
        id1 = request.data.get('licence')
        gen = request.data.get('gender')
        con = request.data.get('contact')
        user = User.objects.create(username=u, first_name=f, last_name=l)
        user.set_password(p)
        user.save()
        sign = Customer.objects.create(user=user, mobile=con, image=i, gender=gen, id_card_no=id1)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'key': token.key},
                        status=HTTP_200_OK)


class login(APIView):

    def post(self, request):
        u = request.data.get('uname')
        p = request.data.get('pwd')
        user = authenticate(username=u, password=p)
        cust = Customer.objects.get(user=user)

        if u is None or p is None:
            return Response({'error': 'Please provide both username and password'}, status=HTTP_400_BAD_REQUEST)

        if user:
            if cust.status.status == "Accept":
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'key': token.key},
                                status=HTTP_200_OK)
            else:
                return Response({'error': "Admin not accept request"})


class Admin_login(APIView):

    def post(self, request):

        u = request.data.get('uname')
        p = request.data.get('pwd')
        user = authenticate(username=u, password=p)
        if user.is_staff:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'key': token.key},
                            status=HTTP_200_OK)
        else:
            return Response({"error": "User is not an admin"},
                            status=HTTP_200_OK)


class Admin_home(APIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = User.objects.get(username=request.user).id
        q = Appointment.objects.all()
        new = 0
        confirm = 0
        total = 0

        if user_id is None:
            return Response({"message": "User id is not given"},
                            status=HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=user_id)
        if user:
            if user.is_staff:
                for i in q:
                    if i.status.status == "pending":
                        new += 1
                    elif i.status.status == "Accept":
                        confirm += 1
                    total += 1
            else:
                return Response({"message": "Please logged in as Admin"},
                                status=HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "User is not logged in"},
                            status=HTTP_400_BAD_REQUEST)
        return Response({"new": new, "confirm": confirm, "total": total},
                        status=HTTP_200_OK)
