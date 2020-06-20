from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from api.models import User_status, Customer


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

