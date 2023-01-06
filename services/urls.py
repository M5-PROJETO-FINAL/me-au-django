from django.urls import path

from . import views

urlpatterns = [
    path("services/", views.ServiceView.as_view()),
    path("services/<int:service_id>/", views.ServiceDetailView.as_view()),

]
