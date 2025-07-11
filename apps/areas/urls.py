"""Areas application URL configuration for Django."""

from .views import AreaDetailView, AreaListView
from django.urls import path

urlpatterns = [
    path("", AreaListView.as_view(), name="area-list"),
    path("<str:slug>/", AreaDetailView.as_view(), name="area-detail"),
]
