from reviews.models import Reviews
from reviews.serializers import ReviewSerializer
from users.models import User
from tests.factories.reservation_factories import create_concluded_reservation



def create_review(
    user: User = None, review_data: dict = None
) -> Reviews:
    reservation = create_concluded_reservation(user=user)

    if not review_data:
        review_data = {
            "review_text": "Review text",
            "stars": 3,
            "reservation": {reservation.id},
        }

    serializer = ReviewSerializer(data=review_data)
    serializer.is_valid(raise_exception=True)

    result = serializer.save(user=user, reservation=reservation)

    return result

