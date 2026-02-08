from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from api.views import PatientViewSet, VeterinarianViewSet, AppointmentViewSet, MedicalRecordViewSet, VaccinationViewSet
from appointments import views as appointments_views

# Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Vet Clinic Api",
        default_version='v1',
        description="Api for vet clinic",
    ),
    public=True,
    permission_classes=[AllowAny],
)

# Api Router
router = routers.DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'veterinarians', VeterinarianViewSet) 
router.register(r'appointments', AppointmentViewSet) 
router.register(r'medical-records', MedicalRecordViewSet)
router.register(r'vaccinations', VaccinationViewSet)

urlpatterns = [
    path('', include('patients.urls')),

    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('appointments/<int:id>/', appointments_views.appointment_detail, name='appointment_detail'),
    path('api-auth/', include('rest_framework.urls')),

    path('appointments/', include('appointments.urls')),
    path('medical/', include('medical_cards.urls')),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
]
