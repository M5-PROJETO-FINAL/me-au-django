from datetime import datetime
from .models import Reservation

class UpdateReservationStatusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):
        self.update_reservation_statuses()
        
        response = self.get_response(request)

        return response


    def update_reservation_statuses(self):
        reservations = Reservation.objects.all()

        today = datetime.now()

        for reservation in reservations:
            checkin = reservation.checkin
            checkout = reservation.checkout

            if reservation.status == "reserved" and today.date() > checkin and today.date() < checkout:
                reservation.status = "active"
                reservation.save()
            elif reservation.status == "active" and today.date() >= checkout:
                reservation.status = "concluded"
                reservation.save()

