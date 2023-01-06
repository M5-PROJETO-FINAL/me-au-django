from django.urls import path
from . import views


urlpatterns = [
    path("reviews/", views.ReviewView.as_view()),
    path("reviews/<uuid:pk>/", views.ReviewDetailView.as_view())
]