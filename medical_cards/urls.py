from django.urls import path
from .views import PatientMedicalCardView, AddMedicalRecordView

urlpatterns = [
    path('<int:patient_id>/', PatientMedicalCardView.as_view(), name='patient_medical_card'),
    path('<int:patient_id>/add-record/', AddMedicalRecordView.as_view(), name='add_medical_record'),
]