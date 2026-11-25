from django.urls import path
from . import api, views

urlpatterns = [
    path("api/get/", api.Dlist, name="json"),
    path("api/post/", api.Dhtviews.as_view(), name="create"),
    path("api/latest/", api.Dlatest, name="dht-latest"),
    path("list/", api.Dlist, name="dht-list"),
    path("dashboard/", views.dashboard, name="dashboard"),
]