from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(
    r'job', views.JobViewSet, basename='job',
)

urlpatterns = [
    path('', include(router.urls)),
]
