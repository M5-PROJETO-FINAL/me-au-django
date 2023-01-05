from django.urls import path
from . import views


urlpatterns = [
    path("reviews/", views.ReviewView.as_view()),
    path("reviews/<pk>/", views.ReviewDetailView.as_view())
]