from .views import AreaListView, AreaDetailView
from django.urls import path


urlpatterns = [
    path("", AreaListView.as_view(), name="area-list"),
    path("<str:pk>/", AreaDetailView.as_view(), name="area-detail"),
]
