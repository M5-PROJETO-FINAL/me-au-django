from services.models import Service


def create_service_with_user(
    # user: User,
    service_data: dict = None,
) -> Service:
        service_test = Service.objects.create(**service_data)

        return service_test
