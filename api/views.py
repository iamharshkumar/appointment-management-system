from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED

from api.models import Customer
from api.serializers import *


class Signup(APIView):

    def post(self, request):
        f = request.data.get('fname')
        l = request.data.get('lname')
        u = request.data.get('uname')
        try:
            user = User.objects.get(username=u)
            return Response({"message": "Username already exits"}, HTTP_200_OK)
        except:
            pass
        i = request.data.get('image')
        p = request.data.get('pwd')
        id1 = request.data.get('licence')
        gen = request.data.get('gender')
        con = request.data.get('contact')
        sta = "Pending"
        user = User.objects.create(username=u, first_name=f, last_name=l)
        user.set_password(p)
        user.save()
        sign = Customer.objects.create(status=sta, user=user, mobile=con, image=i, gender=gen, id_card_no=id1)
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
                    if i.status == "Pending":
                        new += 1
                    elif i.status == "Accept":
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


class View_user(APIView):
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        pro = Customer.objects.all()

        serializer = self.serializer_class(pro, many=True).data
        return Response(serializer, HTTP_200_OK)


class View_New_user(APIView):
    serializer_class = CustomerSerializer
    permission_classes = IsAuthenticated, IsAdminUser

    def get(self, request):
        q = Customer.objects.filter(status="Pending")

        serializer = self.serializer_class(q, many=True).data
        return Response(serializer, HTTP_200_OK)


class Assign_user_status(APIView):
    permission_classes = IsAuthenticated, IsAdminUser

    def post(self, request):
        status = request.data.get("status")
        customer_id = request.data.get("cust_id")
        customer = Customer.objects.get(id=customer_id)
        customer.status = status
        customer.save()
        return Response({"message": "User status changed successfully"}, HTTP_200_OK)


class View_New_Appointment(APIView):
    serializer_class = AppointmentSerializer
    permission_classes = IsAuthenticated, IsAdminUser

    def get(self, request):
        q = Appointment.objects.filter(status="Pending")
        serializer = self.serializer_class(q, many=True).data
        return Response(serializer, HTTP_200_OK)


class View_Confirm_Appointment(APIView):
    serializer_class = AppointmentSerializer
    permission_classes = IsAuthenticated, IsAdminUser

    def get(self, request):
        q = Appointment.objects.filter(status="Accept")
        serializer = self.serializer_class(q, many=True).data
        return Response(serializer, HTTP_200_OK)


class All_Appointment(APIView):
    serializer_class = AppointmentSerializer
    permission_classes = IsAuthenticated, IsAdminUser

    def get(self, request):
        q = Appointment.objects.all()
        serializer = self.serializer_class(q, many=True).data
        return Response(serializer, HTTP_200_OK)


class Assign_book_status(APIView):
    serializer_class = AppointmentSerializer
    permission_classes = IsAuthenticated, IsAdminUser

    def post(self, request):
        appointment_id = request.data.get("apt_id")
        status = request.data.get('status')
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.status = status
        appointment.save()

        return Response({"message": "Appointment status changed successfully"}, HTTP_200_OK)


class View_service(APIView):
    serializer_class = ServiceSerializer

    def get(self, request):
        q = Service.objects.all()
        serializer = self.serializer_class(q, many=True).data
        return Response(serializer, HTTP_200_OK)


class Add_service(APIView):
    permission_classes = IsAuthenticated, IsAdminUser

    def post(self, request):
        name = request.data.get("name")
        cost = request.data.get("cost")
        image = request.data.get("image")
        if name is None or cost is None or image is None:
            return Response({"message": "Please fill out all the fields"}, HTTP_400_BAD_REQUEST)

        Service.objects.create(name=name, cost=cost, image=image)
        return Response({"message": "Service has been created successfully"}, HTTP_201_CREATED)


class Profile(APIView):
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user = User.objects.get(username=request.user).id
        customer = Customer.objects.get(user=user)
        serializer = self.serializer_class(customer).data
        return Response(serializer, HTTP_200_OK)


class Edit_profile(APIView):
    permission_classes = [IsAuthenticated, ]

    def patch(self, request):
        user = User.objects.get(username=request.user)
        customer = Customer.objects.get(user=user)

        f = request.data.get('fname')
        l = request.data.get('lname')
        u = request.data.get('uname')
        i = request.data.get('image')

        id1 = request.data.get('licence')
        con = request.data.get('contact')
        try:
            user = User.objects.get(username=u)
            return Response({"message": "Username already exits"}, HTTP_200_OK)
        except User.DoesNotExist:
            user.username = u

        user.first_name = f
        user.last_name = l
        customer.image = i
        customer.id_card_no = id1
        customer.mobile = con
        user.save()
        customer.save()
        return Response({"message": "Profile update successful"}, HTTP_200_OK)


class Book_appointment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = User.objects.get(username=request.user)
        customer = Customer.objects.get(user=user)
        paid = request.data.get('booking')
        service_id = request.data.get("service")
        service = Service.objects.get(id=service_id)
        booking = Booking_Paid.objects.get(id=paid)
        date = request.data.get('date')
        time = request.data.get('time')
        status = "Pending"
        Appointment.objects.create(service=service, customer=customer, status=status, paid=booking,
                                   date1=date, time1=time)
        return Response({"message": "Appointment create successfully"}, status=HTTP_201_CREATED)
