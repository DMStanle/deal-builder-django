from django.urls import path
from .views import builder_view

urlpatterns = [
    path("", builder_view, name="builder"),
]