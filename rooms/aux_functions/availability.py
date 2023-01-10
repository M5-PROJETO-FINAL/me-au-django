from django.shortcuts import get_object_or_404
from rooms.models import Room, RoomType
from reservations.models import Reservation
from .dates import are_dates_conflicting, get_dates_in_range
from django.core.exceptions import ValidationError
from rest_framework.views import Response
import ipdb

class RoomUnavailable(Exception):
    ...


def get_all_reservations_of_a_given_room_type(room_type_id):
    """
    Returns a list of all reservations made for a particular room type,
    specified by the parameter. Does not include cancelled or concluded reservations.
    """
    room_type = RoomType.objects.get(id=room_type_id)

    # get all reservations that include the shared room::
    all_reservations = Reservation.objects.filter(
        status__in=["reserved", "active"]
    ).all()

    reservations_of_same_room_type = []
    for res in all_reservations:
        for res_pet in res.reservation_pets.all():
            if res_pet.room.room_type == room_type:
                reservations_of_same_room_type.append(res)
                break

    return reservations_of_same_room_type


def get_all_reservations_dates_of_a_given_room_type(room_type_id):
    """
    Returns an array with all reservations dates made for a particular room type,
    specified by the parameter. Does not include cancelled or concluded reservations.
    """
    reservations = get_all_reservations_of_a_given_room_type(room_type_id)
    dates = []
    for reservation in reservations:
        dates = dates + get_dates_in_range(reservation.checkin, reservation.checkout)
    return dates


def get_shared_room_population(date):
    """
    Returns the number of pets occuppying the shared room in a give date,
    specified by the parameter
    """
    shared_room_type = RoomType.objects.get(title="Quarto Compartilhado")
    shared_room = Room.objects.get(room_type=shared_room_type)
    shared_room_reservations = get_all_reservations_of_a_given_room_type(
        shared_room_type.id
    )

    conflicting_reservations = [
        res
        for res in shared_room_reservations
        if res.checkin <= date and res.checkout > date
    ]

    count = 0
    for res in conflicting_reservations:
        for res_pet in res.reservation_pets.all():
            if res_pet.room == shared_room:
                count += 1
    return count

def exists_available_room(date, room_type_id):
    """
    Returns true if there is at least one room of the desired type available in the desired date.
    """
    room_type_reservations = get_all_reservations_of_a_given_room_type(room_type_id)
    room_type_reservations_with_conflicting_date = [res for res in room_type_reservations if res.checkin <= date and res.checkout > date]


    if len(room_type_reservations_with_conflicting_date) >= 4: return False

    amount_of_occupied_rooms = 0
    for res in room_type_reservations_with_conflicting_date:

        occupied_room_ids = []
        for res_pet in res.reservation_pets.all():
            if res_pet.room.room_type_id == room_type_id and res_pet.room.id not in occupied_room_ids:
                occupied_room_ids.append(res_pet.room.id)   
        amount_of_occupied_rooms += len(occupied_room_ids)
    
    return amount_of_occupied_rooms < 4

def get_available_room(
    checkin, checkout, room_type_id, current_reservation_pets
) -> Room:
    """
    Returns a room of a specific type (specified by room_type_id) which is available (has no reservations) in a given time window (specified by checkin and checkout).
    If room_type_id refers to the shared room, the shared room will be returned if and only if it is operating below its full capacity (of 20 dogs) for all dates in the specified range.
    """
    room_type = get_object_or_404(RoomType, id=room_type_id)
    all_rooms = Room.objects.filter(room_type=room_type)
    required_dates = get_dates_in_range(checkin, checkout)

    if room_type.title == "Quarto Compartilhado":
        for date in required_dates:
            population = get_shared_room_population(date)
            if population >= room_type.capacity:
                raise RoomUnavailable(f"Shared room is full on {date}")
        shared_room = all_rooms.first()
        return shared_room

    reservations_of_same_room_type = get_all_reservations_of_a_given_room_type(
        room_type_id
    )
    conflicting_reservations = [
        res
        for res in reservations_of_same_room_type
        if are_dates_conflicting(checkin, checkout, res.checkin, res.checkout)
    ]
    # quartos já ocupados NESSA reserva q está sendo criada
    already_occupied_rooms_ids = [
        res_pet.room.id for res_pet in current_reservation_pets
    ]

    ids_of_available_rooms = [
        room.id for room in all_rooms if room.id not in already_occupied_rooms_ids
    ]

    # ultimo filtro para quartos possíveis: remover quartos q estão em conflicting_reservations
    for reservation in conflicting_reservations:
        for res_pet in reservation.reservation_pets.all():
            if res_pet.room.id in ids_of_available_rooms:
                idx = ids_of_available_rooms.index(res_pet.room.id)
                ids_of_available_rooms.pop(idx)
    if len(ids_of_available_rooms) == 0:
        raise RoomUnavailable(f"No rooms of type '{room_type.title}' available")

    return Room.objects.get(id=ids_of_available_rooms[0])
