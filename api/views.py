from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from api.models import User_status, Customer


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def Signup(request):
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


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
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
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'key': token.key},
                    status=HTTP_200_OK)

