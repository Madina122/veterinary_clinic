from django.urls import path
from .views import BookAppointmentView
from . import views

urlpatterns = [
    path('book/', BookAppointmentView.as_view(), name='book_appointment'),
    path('<int:id>/', views.appointment_detail, name='appointment_detail'), 
]