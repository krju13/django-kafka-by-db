from django.urls import path
from .views import manage_rest

urlpatterns = [
    path('api/', manage_rest.as_view(), name="api"),
]
