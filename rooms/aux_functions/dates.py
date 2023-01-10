from datetime import datetime, timedelta
from typing import List

def get_min_and_max_dates(reservations):
    """
    Given a list of reservations, returns the dates of the earliest checkin and the latest checkout among those reservations.
    Return format:
    earliestCheckin, latestCheckout
    """
    if len(reservations) == 0:
        now = datetime.now().date()
        return [now, now]
    
    min_checkin = reservations[0].checkin
    max_checkout = reservations[0].checkout
    for reservation in reservations:
        if reservation.checkin < min_checkin:
            min_checkin = reservation.checkin
        if reservation.checkout > max_checkout:
            max_checkout = reservation.checkout
    return min_checkin, max_checkout


def get_dates_in_range(min_date: datetime, max_date: datetime) -> List[datetime]:
    """
    Returns a list of dates with all days spanning a given range, starting from minDate and ending on maxDate (inclusive)

    Example:

    get_dates_in_range('2010-01-20', '2010-01-24')
    returns:
    ['2010-01-20', '2010-01-21', '2010-01-22', '2010-01-23', '2010-01-24']
    (except that dates are actually datetime objects instead of strings)
    """
    dates = []
    curr_date = min_date
    while curr_date < max_date:
        dates.append(curr_date)
        curr_date += timedelta(1)
    return dates


def are_dates_conflicting(
    checkin1: datetime, checkout1: datetime, checkin2: datetime, checkout2: datetime
):
    """
    Returns true if the time interval specified by the first pair of parameters is somehow conflicting with the time interval specified by the second pair of parameters.
    """
    return (
        (checkout2 > checkin1 and checkout2 <= checkout1)
        or (checkin2 >= checkin1 and checkin2 < checkout1)
        or (checkin2 <= checkin1 and checkout2 >= checkout1)
    )
