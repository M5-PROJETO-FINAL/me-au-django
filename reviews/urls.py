from django.urls import path
from . import views


urlpatterns = [
    path("reviews/", views.ReviewView),
    path("reviews/<int:pk>/", views.ReviewDetailView)
]