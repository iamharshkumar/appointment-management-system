from django.urls import path
from .views import *

urlpatterns = [
    path('signup', Signup.as_view(), name='signup'),
    path('login', login.as_view(), name='login'),
    path('admin-login', Admin_login.as_view(), name='admin-login'),
    path('admin-home', Admin_home.as_view(), name='admin-home'),
    path('view-user', View_user.as_view(), name='view-user'),
    path('view-new-user', View_New_user.as_view(), name='view-new-user'),
    path('assign-user-status', Assign_user_status.as_view(), name='assign-user-status'),
    path('assign-appointment-status', Assign_book_status.as_view(), name='assign-appointment-status'),
    path('view-new-appointment', View_New_Appointment.as_view(), name='view-new-appointment'),
    path('view-confirm-appointment', View_Confirm_Appointment.as_view(), name='view-confirm-appointment'),
    path('all-appointment', All_Appointment.as_view(), name='all-appointment'),
    path('view-service', View_service.as_view(), name='view-service'),
    path('add-service', Add_service.as_view(), name='add-service'),
    path('user-profile', Profile.as_view(), name='user-profile'),
    path('edit-profile', Edit_profile.as_view(), name='edit-profile'),
    path('book-appointment', Book_appointment.as_view(), name='book-appointment'),
    path('delete-appointment', delete_appointment.as_view(), name='delete-appointment'),
    path('delete-service', delete_service.as_view(), name='delete-service'),
    path('delete-user', delete_user.as_view(), name='delete-user'),

]
