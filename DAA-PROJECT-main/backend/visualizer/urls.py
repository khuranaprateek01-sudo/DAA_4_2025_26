from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/health/", views.health, name="health"),
    path("api/sort/benchmark/", views.sort_benchmark_endpoint, name="sort-benchmark-endpoint"),
    path("api/sort/<str:algo>/", views.sort_endpoint, name="sort-endpoint"),
    path("api/graph/<str:algo>/", views.graph_endpoint, name="graph-endpoint"),
    path("api/dp/knapsack/", views.knapsack_endpoint, name="knapsack-endpoint"),
    path("api/dp/lcs/", views.lcs_endpoint, name="lcs-endpoint"),
    path("api/history/", views.history_endpoint, name="history-endpoint"),
]
