from django.urls import path
from .views import (
    AddPatientView, 
    PatientListView,
    HomeView  
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),  
    path('patients/', PatientListView.as_view(), name='patient_list'),
    path('add/', AddPatientView.as_view(), name='add_patient'),
]